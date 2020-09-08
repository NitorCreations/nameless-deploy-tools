#/bin/bash -x
if ! grep -e 'secure_path.*/usr/local/bin' /etc/sudoers > /dev/null; then
    sed -i 's/\(.*secure_path.*\)/\1:\/usr\/local\/bin/' /etc/sudoers
fi
exit 0
