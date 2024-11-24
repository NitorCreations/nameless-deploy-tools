#!/bin/bash
set -eo pipefail

USAGE="Usage: $0 [OPTIONS]

Compile faster register complete binaries for ndt.

OPTIONS: All options are optional
  -h | --help
    Display these instructions.

  -d | --dryrun
    Only print commands instead of executing them.

  -v | --verbose
    Display commands being executed."

init_options() {
  DRYRUN=false
  while [ $# -gt 0 ]; do
    case "$1" in
      -h | --help)
        echo "$USAGE"
        exit 1
        ;;
      -d | --dryrun)
        DRYRUN=true
        ;;
      -v | --verbose)
        set -x
        ;;
    esac
    shift
  done
}

init_options "$@"

# Import common functions
DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=./common.sh
source "$DIR/common.sh"

print_magenta "Compiling faster shell completitions..."

ARGS=(-std=c++20 -O3 -Wall -Wextra -march=native -mtune=native)
COMPILER="g++"

if [ -z "$(command -v "$COMPILER")" ]; then
  print_error_and_exit "Compiler not found: $COMPILER"
fi

$COMPILER --version

for file in nameless-dt-register-complete nameless-dt-print-aws-profiles; do
  if [ -n "$(command -v $file)" ]; then
    print_yellow "Overwriting existing script: $file"
    DESTINATION="$(which $file)"
  else
    check_and_set_python
    DESTINATION="$(dirname "$PYTHON")/$file"
  fi
  print_magenta "Compiling ${file}.cpp"
  run_command $COMPILER "${ARGS[@]}" "$REPO_ROOT/n_utils/${file}.cpp" -o "$DESTINATION"
done
