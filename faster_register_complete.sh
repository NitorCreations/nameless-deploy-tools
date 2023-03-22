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

ARGS=(-std=c++20 -O3 -Wall -Wextra)

if [ "$PLATFORM" = mac ]; then
  # 03/2023:
  # try to use brew llvm / Clang since it is newer than what Apple includes.
  # Critically, Clang 14 does not yet support `march` compiler option for Apple Silicon,
  # but brew llvm comes with Clang 15 that does support it so we can get the full benefit from the C++ code.
  # This can be removed once macOS comes with Clang 15 by default...
  if [ -e "$(brew --prefix)/opt/llvm/bin/clang++" ]; then
    COMPILER="$(brew --prefix)/opt/llvm/bin/clang++"
    ARGS+=(-march=native -mtune=native)
  else
    echo "You might want to install the latest Clang from brew ('brew install llvm') to get the best results..."
    COMPILER="g++"
  fi
else
  COMPILER="g++"
  ARGS+=(-march=native -mtune=native)
fi

if [ -n "$(command -v nameless-dt-register-complete)" ]; then
  print_yellow "Overwriting existing script: nameless-dt-register-complete"
  DESTINATION="$(which nameless-dt-register-complete)"
else
  check_and_set_python
  DESTINATION="$(dirname "$PYTHON")/nameless-dt-register-complete"
fi

if [ -z "$(command -v "$COMPILER")" ]; then
  echo "Compiler not found: $COMPILER"
  exit 1
fi

$COMPILER --version

print_magenta "Compiling nameless-dt-register-complete.cpp"
run_command $COMPILER "${ARGS[@]}" "$REPO_ROOT/n_utils/nameless-dt-register-complete.cpp" -o "$DESTINATION"

print_magenta "Compiling nameless-dt-print-aws-profiles.cpp"
DESTINATION="$(dirname "$DESTINATION")/nameless-dt-print-aws-profiles"
run_command $COMPILER "${ARGS[@]}" "$REPO_ROOT/n_utils/nameless-dt-print-aws-profiles.cpp" -o "$DESTINATION"
