import json

from n_utils.profile_util import enable_profile, get_profile, read_profiles


def test_get_profile():
    profile = get_profile("foo89432890")
    assert not profile


def test_read_profiles():
    profiles = read_profiles()
    print(json.dumps(profiles))


def test_iam_profile_switch(capsys):
    enable_profile("iam", "testprofile")
    captured = capsys.readouterr()
    assert 'AWS_PROFILE="testprofile"' in captured.out


def test_azure_profile_switch(capsys):
    enable_profile("azure", "testprofile")
    captured = capsys.readouterr()
    assert "aws-azure-login --profile testprofile" in captured.out


def test_adfs_profile_switch(capsys):
    enable_profile("adfs", "testprofile")
    captured = capsys.readouterr()
    assert "adfs-aws-login --profile testprofile" in captured.out


def test_adfs_profile_switch(capsys):
    enable_profile("lastpass", "testprofile")
    captured = capsys.readouterr()
    assert "lastpass-aws-login --profile testprofile"
