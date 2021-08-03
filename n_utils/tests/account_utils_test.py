from n_utils.account_utils import find_role_arn


def test_find_role_arn(mocker):
    cloudformation = mocker.patch("n_utils.account_utils.cloudformation")

    find_role_arn("foo")

    cloudformation.assert_called_with()
