#!/bin/bash

sudo -H pip install -U nuitka
ENV_SCRIPT="$(dirname $(dirname $(n-include hook.sh)))/nameless-dt-load-project-env.py"
PROFILE_SCRIPT="$(dirname $(dirname $(n-include hook.sh)))/nameless-dt-enable-profile.py"
python -m nuitka --follow-imports $ENV_SCRIPT
python -m nuitka --follow-imports $PROFILE_SCRIPT
sudo cp nameless-dt-load-project-env.bin $(which nameless-dt-load-project-env)
sudo cp nameless-dt-enable-profile.bin $(which nameless-dt-enable-profile)
