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
  echo "usage: mount-and-format.sh [-h] blk-device mount-path" >&2
  echo "" >&2
  echo "Mounts a local block device as an encrypted volume. Handy for things like local database installs."
  echo "" >&2
  echo "positional arguments" >&2
  echo "  blk-device  the block device you want to mount and formant" >&2
  echo "  mount-path  the mount point for the volume" >&2
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

# Check arguments
if ! [ -b "$1" ]; then
  usage "'$1' not a block device"
fi
if ! ([ -d "$2" ] || mkdir -p "$2"); then
  usage "Mount point $2 not available"
fi
DEVPATH=$1
MOUNT_PATH=$2
# Make sure the device is not already directly mounted
umount -f $DEVPATH
# Make sure the mount path is not already mounted
umount -f $MOUNT_PATH
# Create a filesystem
mkfs.ext4 $DEVPATH
# Mount
mount $DEVPATH $MOUNT_PATH
