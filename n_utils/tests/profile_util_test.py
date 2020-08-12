from n_utils.profile_util import get_profile, read_profiles
import json

def test_get_profile():
    profile = get_profile("foo89432890")
    assert not profile

def test_read_profiles():
    profiles = read_profiles()
    print(json.dumps(profiles))    