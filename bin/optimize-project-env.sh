#!/bin/bash

sudo -H pip install -U nuitka
ENV_SCRIPT="$(dirname $(dirname $(n-include hook.sh)))/nameless-dt-load-project-env.py"
PROFILE_SCRIPT="$(dirname $(dirname $(n-include hook.sh)))/nameless-dt-enable-profile.py"
python -m nuitka --recurse-to=n_utils.project_util --follow-import-to=n_utils.profile_util --follow-import-to=n_utils $ENV_SCRIPT
python -m nuitka --follow-import-to=n_utils.profile_util --follow-import-to=n_utils $PROFILE_SCRIPT
sudo cp nameless-dt-load-project-env.bin $(which nameless-dt-load-project-env)
sudo cp nameless-dt-enable-profile.bin $(which nameless-dt-enable-profile)
