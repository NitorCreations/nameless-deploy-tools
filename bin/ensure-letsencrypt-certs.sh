#!/bin/bash

# Copyright 2016-2017 Nitor Creations Oy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

if [ "$_ARGCOMPLETE" ]; then
  # Handle command completion executions
  exit 0
fi

usage() {
  echo "usage: ensure-letsencrypt-certs.sh [-h] domain-name [domain-name ...]" >&2
  echo "" >&2
  echo "Fetches a certificate with fetch-secrets.sh, and exits cleanly if certificate is found and valid." >&2
  echo "Otherwise gets a new certificate from letsencrypt via DNS verification using Route53." >&2
  echo "Requires that fetch-secrets.sh and Route53 are set up correctly." >&2
  echo "" >&2
  echo "positional arguments" >&2
  echo "  domain-name   The domain(s) you want to check certificates for" >&2
  echo "" >&2
  echo "optional arguments:" >&2
  echo "  -h, --help  show this help message and exit" >&2
  exit 1
}

if [ "$1" = "--help" -o "$1" = "-h" ]; then
  usage
fi

if [ -z "$1" ]; then
  usage
fi

cleanup() {
  fetch-secrets.sh logout
}
trap cleanup EXIT

RENEW_DAYS="30"
if [ -z "$CERT_DIR" ]; then
  CERT_DIR=/etc/certs
fi
mkdir -p $CERT_DIR
renew_cert() {
  local DOMAIN="$1"
  echo "LOCKFILE=$CERT_DIR/lock" > $CERT_DIR/conf
  if [ -n "$ACCOUNTDIR" ]; then
    echo "ACCOUNTDIR=$ACCOUNTDIR" >> $CERT_DIR/conf
  else
    echo "ACCOUNTDIR=$HOME/.letsencrypt/" >> $CERT_DIR/conf
  fi
  export CONFIG="$CERT_DIR/conf"
  $(n-include letsencrypt.sh) --register --accept-terms
  $(n-include letsencrypt.sh) --cron --hook $(n-include hook.sh) --challenge dns-01 --domain "$DOMAIN"
}

for DOMAIN in "$@"; do
  CERT=$CERT_DIR/$DOMAIN.crt
  if [ -e $CERT ]; then
    chmod 600 $CERT
  fi
  if fetch-secrets.sh get 444 $CERT; then
    VALID="$(openssl x509 -enddate -noout -in "$CERT" | cut -d= -f2-)"
    echo "Valid: $VALID"
    if ! openssl x509 -checkend $((RENEW_DAYS * 86400)) -noout -in "$CERT"; then
      renew_cert $DOMAIN
    fi
  else
    renew_cert $DOMAIN
  fi
done
