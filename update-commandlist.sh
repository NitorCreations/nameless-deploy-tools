#!/bin/bash
set -exo pipefail

printf "# NDT Command Reference\n\n" > docs/commands.md
./document_commands.py >> docs/commands.md
