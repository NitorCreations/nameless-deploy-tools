#!/bin/bash

echo "You need to install nuitka (pip), gcc, ccache and chrpath (apt, yum, brew or snap) for this to work"

ENV_SCRIPT="$(dirname $(dirname $(n-include hook.sh)))/nameless-dt-load-project-env.py"
PROFILE_SCRIPT="$(dirname $(dirname $(n-include hook.sh)))/nameless-dt-enable-profile.py"
python -m nuitka --follow-imports $ENV_SCRIPT
python -m nuitka --follow-imports $PROFILE_SCRIPT
cp nameless-dt-load-project-env.bin $(which nameless-dt-load-project-env)
cp nameless-dt-enable-profile.bin $(which nameless-dt-enable-profile)
