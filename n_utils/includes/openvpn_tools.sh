#!/bin/bash -e

source $(n-include common_tools.sh)

if [ -z "$EASYRSA_VERSION" ]; then
  EASYRSA_VERSION=3.0.8
fi

openvpn_install_easyrsa() {
  check_parameters CF_paramDnsName
  add_gpg_key C8FCA3E7F787072CDEB91D2F72964219390D0D0E
  gpg_safe_download "https://github.com/OpenVPN/easy-rsa/releases/download/v$EASYRSA_VERSION/EasyRSA-$EASYRSA_VERSION.tgz" easy-rsa.tgz
  mkdir -p /etc/openvpn/easy-rsa
  tar -xzvf easy-rsa.tgz --strip-components=1 --directory /etc/openvpn/easy-rsa
  rm -f easy-rsa.tgz.sig easy-rsa.tgz
  cd /etc/openvpn/easy-rsa/ || return
  echo "set_var EASYRSA_ALGO ec" > vars
  echo "set_var EASYRSA_CURVE prime256v1" >> vars
  fetch-secrets.sh get 500 --optional /etc/openvpn/easy-rsa/${CF_paramDnsName}-easyrsa-keys.sh
  if [ -x /etc/openvpn/easy-rsa/${CF_paramDnsName}-easyrsa-keys.sh ]; then
    /etc/openvpn/easy-rsa/${CF_paramDnsName}-easyrsa-keys.sh
    SERVER_NAME=$(cat SERVER_NAME_GENERATED)
    SERVER_CN=$(cat SERVER_CN_GENERATED)
    echo "set_var EASYRSA_REQ_CN $SERVER_CN" >> vars
  else
    # Generate a random, alphanumeric identifier of 16 characters for CN and one for server name
    SERVER_CN="cn_$(head /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1)"
    echo "$SERVER_CN" > SERVER_CN_GENERATED
    SERVER_NAME="server_$(head /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1)"
    echo "$SERVER_NAME" > SERVER_NAME_GENERATED

    echo "set_var EASYRSA_REQ_CN $SERVER_CN" >> vars

    # Create the PKI, set up the CA, the DH params and the server certificate
    ./easyrsa init-pki
    ./easyrsa --batch build-ca nopass

    ./easyrsa build-server-full "$SERVER_NAME" nopass
    EASYRSA_CRL_DAYS=3650 ./easyrsa gen-crl

    # Generate tls-crypt key
    openvpn --genkey --secret /etc/openvpn/tls-crypt.key
    openvpn_secrets_store_message
  fi

  # Move all the generated files
  \cp --force pki/ca.crt pki/private/ca.key "pki/issued/$SERVER_NAME.crt" "pki/private/$SERVER_NAME.key" /etc/openvpn/easy-rsa/pki/crl.pem /etc/openvpn

  # Make cert revocation list readable for non-root
  chmod 644 /etc/openvpn/crl.pem
}
openvpn_secrets_store_message() {
  check_parameters CF_paramDnsName
  local SERVER_NAME=$(cat /etc/openvpn/easy-rsa/SERVER_NAME_GENERATED)
  echo "To make this setup persistent, you should run:"
  echo 'create-shell-archive.sh $(find /etc/openvpn/easy-rsa/pki -type f) \'
  echo "  /etc/openvpn/tls-crypt.key \\"
  echo "  /etc/openvpn/easy-rsa/SERVER_NAME_GENERATED \\"
  echo "  /etc/openvpn/easy-rsa/SERVER_CN_GENERATED > ${CF_paramDnsName}-easyrsa-keys.sh"
  echo "and store that where your secrets are kept. Potentially doable with (if you have the rights to store secrets from here):"
  echo "store-secret.sh ${CF_paramDnsName}-easyrsa-keys.sh < ${CF_paramDnsName}-easyrsa-keys.sh"
}
openvpn_configure() {
  local SERVER_NAME=$(cat /etc/openvpn/easy-rsa/SERVER_NAME_GENERATED)
  local NIC=$(ip -4 route ls | grep default | grep -Po '(?<=dev )(\S+)' | head -1)
  local PROTOCOL=tcp
  local PORT=1194
  local IP=localhost

  cat > /etc/openvpn/server.conf << EOF
port $PORT
proto $PROTOCOL
dev tun
user nobody
group nobody
persist-key
persist-tun
keepalive 10 120
topology subnet
server 10.8.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt
dh none
ecdh-curve prime256v1
tls-crypt tls-crypt.key
crl-verify crl.pem
ca ca.crt
cert ${SERVER_NAME}.crt
key ${SERVER_NAME}.key
auth SHA256
cipher AES-128-GCM
ncp-ciphers AES-128-GCM
tls-server
tls-version-min 1.2
tls-cipher TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256
client-config-dir /etc/openvpn/ccd
status /var/log/openvpn/status.log
verb 3
EOF

  if grep -q "127.0.0.53" "/etc/resolv.conf"; then
    RESOLVCONF='/run/systemd/resolve/resolv.conf'
  else
    RESOLVCONF='/etc/resolv.conf'
  fi
  # Obtain the resolvers from resolv.conf and use them for OpenVPN
  sed -ne 's/^nameserver[[:space:]]\+\([^[:space:]]\+\).*$/\1/p' $RESOLVCONF | while read -r line; do
    # Copy, if it's a IPv4
    if [[ $line =~ ^[0-9.]*$ ]]; then
      echo "push \"dhcp-option DNS $line\"" >> /etc/openvpn/server.conf
    fi
  done
  # Create client-config-dir dir
  mkdir -p /etc/openvpn/ccd
  # Create log dir
  mkdir -p /var/log/openvpn

  # Enable routing
  echo 'net.ipv4.ip_forward=1' > /etc/sysctl.d/99-openvpn.conf
  sysctl --system

  source /etc/os-release
  # Finally, restart and enable OpenVPN
  if [[ $ID == 'arch' || $ID == 'fedora' || $ID == 'centos' || $ID == 'oracle' || $ID == 'rocky' ]]; then
    # Don't modify package-provided service
    cp /usr/lib/systemd/system/openvpn-server@.service /etc/systemd/system/openvpn-server@.service

    # Workaround to fix OpenVPN service on OpenVZ
    sed -i 's|LimitNPROC|#LimitNPROC|' /etc/systemd/system/openvpn-server@.service
    # Another workaround to keep using /etc/openvpn/
    sed -i 's|/etc/openvpn/server|/etc/openvpn|' /etc/systemd/system/openvpn-server@.service

    systemctl daemon-reload
    systemctl enable openvpn-server@server
    systemctl restart openvpn-server@server
  elif [[ $ID == "ubuntu" ]] && [[ $VERSION_ID == "16.04" ]]; then
    # On Ubuntu 16.04, we use the package from the OpenVPN repo
    # This package uses a sysvinit service
    systemctl enable openvpn
    systemctl start openvpn
  else
    # Don't modify package-provided service
    cp /lib/systemd/system/openvpn\@.service /etc/systemd/system/openvpn\@.service

    # Workaround to fix OpenVPN service on OpenVZ
    sed -i 's|LimitNPROC|#LimitNPROC|' /etc/systemd/system/openvpn\@.service
    # Another workaround to keep using /etc/openvpn/
    sed -i 's|/etc/openvpn/server|/etc/openvpn|' /etc/systemd/system/openvpn\@.service

    systemctl daemon-reload
    systemctl enable openvpn@server
    systemctl restart openvpn@server
  fi

  # Add iptables rules in two scripts
  mkdir -p /etc/iptables

  # Script to add rules
  cat > /etc/iptables/add-openvpn-rules.sh << EOF
#!/bin/sh
iptables -t nat -I POSTROUTING 1 -s 10.8.0.0/24 -o $NIC -j MASQUERADE
iptables -I INPUT 1 -i tun0 -j ACCEPT
iptables -I FORWARD 1 -i $NIC -o tun0 -j ACCEPT
iptables -I FORWARD 1 -i tun0 -o $NIC -j ACCEPT
iptables -I INPUT 1 -i $NIC -p $PROTOCOL --dport $PORT -j ACCEPT
EOF

  # Script to remove rules
  cat > /etc/iptables/rm-openvpn-rules.sh << EOF
#!/bin/sh
iptables -t nat -D POSTROUTING -s 10.8.0.0/24 -o $NIC -j MASQUERADE
iptables -D INPUT -i tun0 -j ACCEPT
iptables -D FORWARD -i $NIC -o tun0 -j ACCEPT
iptables -D FORWARD -i tun0 -o $NIC -j ACCEPT
iptables -D INPUT -i $NIC -p $PROTOCOL --dport $PORT -j ACCEPT
EOF

  chmod +x /etc/iptables/add-openvpn-rules.sh
  chmod +x /etc/iptables/rm-openvpn-rules.sh

  # Handle the rules via a systemd script
  cat > /etc/systemd/system/iptables-openvpn.service << EOF
[Unit]
Description=iptables rules for OpenVPN
Before=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/etc/iptables/add-openvpn-rules.sh
ExecStop=/etc/iptables/rm-openvpn-rules.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

  # Enable service and apply rules
  systemctl daemon-reload
  systemctl enable iptables-openvpn
  systemctl start iptables-openvpn

  cat > /etc/openvpn/client-template.txt << EOF
client
proto tcp-client
remote $IP $PORT
dev tun
resolv-retry infinite
nobind
persist-key
persist-tun
duplicate-cn
remote-cert-tls server
verify-x509-name $SERVER_NAME name
auth SHA256
auth-nocache
cipher AES-128-GCM
tls-client
tls-version-min 1.2
tls-cipher TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256
ignore-unknown-option block-outside-dns
setenv opt block-outside-dns # Prevent Windows 10 DNS leak
pull-filter ignore "route-gateway"
verb 3
EOF
  if [[ ! -f /etc/openvpn/easy-rsa/pki/issued/ingress.crt ]]; then
    openvpn_new_client "ingress"
  fi
}
function openvpn_add_route() {
  local NET=$1
  local ADDR=$(python -c "from ipaddress import ip_network; print(f\"{ip_network('$NET').network_address}\")")
  local NETMASK=$(python -c "from ipaddress import ip_network; print(f\"{ip_network('$NET').netmask}\")")
  echo "push \"route $ADDR $NETMASK\"" >> /etc/openvpn/server.conf
}
function openvpn_add_domain() {
  echo "push \"dhcp-option DOMAIN $1\"" >> /etc/openvpn/server.conf
}
function openvpn_new_client() {
  local CLIENT=$1
  cd /etc/openvpn/easy-rsa/ || return
  ./easyrsa build-client-full "$CLIENT" nopass
  echo "Client $CLIENT added."

  homeDir="/root"

  # Generates the custom client.ovpn
  cp /etc/openvpn/client-template.txt "$homeDir/$CLIENT.ovpn"
  {
    echo "<ca>"
    cat "/etc/openvpn/easy-rsa/pki/ca.crt"
    echo "</ca>"

    echo "<cert>"
    awk '/BEGIN/,/END/' "/etc/openvpn/easy-rsa/pki/issued/$CLIENT.crt"
    echo "</cert>"

    echo "<key>"
    cat "/etc/openvpn/easy-rsa/pki/private/$CLIENT.key"
    echo "</key>"

    echo "<tls-crypt>"
    cat /etc/openvpn/tls-crypt.key
    echo "</tls-crypt>"
  } >> "$homeDir/$CLIENT.ovpn"

  echo ""
  echo "The configuration file has been written to $homeDir/$CLIENT.ovpn."
}
