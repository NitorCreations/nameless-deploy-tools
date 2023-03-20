#!/bin/bash
set -eo pipefail

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# Check platform
case "$(uname -s)" in
  "Darwin")
    PLATFORM="mac"
    ;;
  "MINGW"*)
    PLATFORM="windows"
    ;;
  *)
    PLATFORM="linux"
    ;;
esac

if [ -n "$(command -v python3)" ]; then
  PYTHON=$(which python3)
else
  PYTHON=$(which python)
fi

if [ ! -e "$PYTHON" ]; then
  echo "Python executable not found: $PYTHON"
  exit 1
else
  echo "Using $PYTHON $($PYTHON --version)"
fi

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
    COMPILER="g++"
  fi
else
  COMPILER="g++"
  ARGS+=(-march=native -mtune=native)
fi

ARGS+=("$REPO_ROOT/n_utils/nameless-dt-register-complete.cpp" -o "$(dirname "$PYTHON")/nameless-dt-register-complete")

if [ -z "$(command -v "$COMPILER")" ]; then
  echo "Compiler not found: $COMPILER"
  exit 1
fi

echo "Running: $COMPILER ${ARGS[*]}"
$COMPILER --version
$COMPILER "${ARGS[@]}"
