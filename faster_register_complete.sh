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

ARGS=(-std=c++20 -O3 -Wall -Wextra -march=native -mtune=native)
COMPILER="g++"

if [ -n "$(command -v nameless-dt-register-complete)" ]; then
  print_yellow "Overwriting existing script: nameless-dt-register-complete"
  DESTINATION="$(which nameless-dt-register-complete)"
else
  check_and_set_python
  DESTINATION="$(dirname "$PYTHON")/nameless-dt-register-complete"
fi

if [ -z "$(command -v "$COMPILER")" ]; then
  print_error_and_exit "Compiler not found: $COMPILER"
fi

$COMPILER --version

print_magenta "Compiling nameless-dt-register-complete.cpp"
run_command $COMPILER "${ARGS[@]}" "$REPO_ROOT/n_utils/nameless-dt-register-complete.cpp" -o "$DESTINATION"

print_magenta "Compiling nameless-dt-print-aws-profiles.cpp"
DESTINATION="$(dirname "$DESTINATION")/nameless-dt-print-aws-profiles"
run_command $COMPILER "${ARGS[@]}" "$REPO_ROOT/n_utils/nameless-dt-print-aws-profiles.cpp" -o "$DESTINATION"
