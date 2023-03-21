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
  case $COMP_CWORD in
    2)
      DEVICES=$(lsblk -pnlo name)
      compgen -W "-h $DEVICES" -- $COMP_CUR
      ;;
    3)
      compgen -f -- $COMP_CUR
      ;;
    *)
      exit 1
      ;;
  esac
  exit 0
fi

usage() {
  echo "usage: encrypt-and-mount.sh [-h] blk-device mount-path" >&2
  echo "" >&2
  echo "Mounts a local block device as an encrypted volume. Handy for things like local database installs."
  echo "" >&2
  echo "positional arguments" >&2
  echo "  blk-device  the block device you want to encrypt and mount" >&2
  echo "  mount-path  the mount point for the encrypted volume" >&2
  echo "" >&2
  echo "optional arguments:" >&2
  echo "  -h, --help  show this help message and exit" >&2
  if [ -n "$1" ]; then
    echo "" >&2
    echo "$1" >&2
  fi
  exit 1
}

if [ "$1" = "--help" -o "$1" = "-h" ]; then
  usage
fi

crypted_devices() {
  for dev in $(dmsetup ls --target crypt | grep -v "No devices found" | awk '{ print $1 }'); do
    echo -n "$dev "
    dmsetup deps $dev -o blkdevname | awk -NF '\\(|\\)' '{ print $2 }'
  done
}
# Check arguments
if ! [ -b "$1" ]; then
  usage "'$1' not a block device"
fi
if ! ([ -d "$2" ] || mkdir -p "$2"); then
  usage "Mount point $2 not available"
fi
DEVPATH=$1
DEV=$(basename $DEVPATH)
MOUNT_PATH=$2
# Make sure the block device is not already mapped
if crypted_devices | grep $DEV > /dev/null; then
  CRYPTDEV=$(crypted_devices | grep $DEV | cut -d" " -f1)
  umount -f /dev/mapper/$CRYPTDEV
  cryptsetup close $CRYPTDEV
fi
# Make sure the device is not already directly mounted
umount -f $DEVPATH
# Find a free mapping
COUNT=1
while [ -e /dev/mapper/e$COUNT ]; do
  COUNT=$(($COUNT + 1))
done
CRYPTDEV=e$COUNT
# Create a random keyfile
TMPDIR=$(mktemp -d)
mount tmpfs $TMPDIR -t tmpfs -o size=32m
touch $TMPDIR/disk.pwd
chmod 600 $TMPDIR/disk.pwd
dd if=/dev/urandom of=$TMPDIR/disk.pwd bs=512 count=4 status=none iflag=fullblock
#Open plain dm-crypt mapping
cryptsetup --cipher=aes-xts-plain64 --key-file=$TMPDIR/disk.pwd --key-size=512 \
  open --type=plain $DEVPATH $CRYPTDEV
# Get rid of keyfile
umount -f $TMPDIR
# Make sure the mount path is not already mounted
umount -f $MOUNT_PATH
# Create a filesystem
mkfs.ext4 /dev/mapper/$CRYPTDEV
# Mount
mount /dev/mapper/$CRYPTDEV $MOUNT_PATH
