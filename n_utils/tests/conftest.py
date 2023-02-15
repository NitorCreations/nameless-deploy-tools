import pytest

BASE_MODULE_NAME = "n_utils"


def get_test_target_module(test_module):
    if test_module.endswith("_test"):
        return test_module[:-5]
    if test_module.startswith("test_"):
        return test_module[5:]
    return test_module


@pytest.fixture(scope="function")
def cloudformation(mocker, request):
    target = f"{BASE_MODULE_NAME}.{get_test_target_module(request.module.__name__)}.cloudformation"
    if load_class(target):
        print(f"Mocking {target}")
        client = mocker.MagicMock()
        client_func = mocker.patch(target)
        client_func.return_value = client
        return client


@pytest.fixture(scope="function")
def cloudfront(mocker, request):
    target = f"{BASE_MODULE_NAME}.{get_test_target_module(request.module.__name__)}.cloudfront"
    if load_class(target):
        print(f"Mocking {target}")
        client = mocker.MagicMock()
        client_func = mocker.patch(target)
        client_func.return_value = client
        return client


@pytest.fixture(scope="function")
def ec2(mocker, request):
    target = f"{BASE_MODULE_NAME}.{get_test_target_module(request.module.__name__)}.ec2"
    if load_class(target):
        print(f"Mocking {target}")
        client = mocker.MagicMock()
        client_func = mocker.patch(target)
        client_func.return_value = client
        return client


@pytest.fixture(scope="function")
def ecr(mocker, request):
    target = f"{BASE_MODULE_NAME}.{get_test_target_module(request.module.__name__)}.ecr"
    if load_class(target):
        print(f"Mocking {target}")
        client = mocker.MagicMock()
        client_func = mocker.patch(target)
        client_func.return_value = client
        return client


@pytest.fixture(scope="function")
def organizations(mocker, request):
    target = f"{BASE_MODULE_NAME}.{get_test_target_module(request.module.__name__)}.organizations"
    if load_class(target):
        print(f"Mocking {target}")
        client = mocker.MagicMock()
        client_func = mocker.patch(target)
        client_func.return_value = client
        return client


@pytest.fixture(scope="function")
def route53(mocker, request):
    target = f"{BASE_MODULE_NAME}.{get_test_target_module(request.module.__name__)}.route53"
    if load_class(target):
        print(f"Mocking {target}")
        client = mocker.MagicMock()
        client_func = mocker.patch(target)
        client_func.return_value = client
        return client


@pytest.fixture(scope="function")
def s3(mocker, request):
    target = f"{BASE_MODULE_NAME}.{get_test_target_module(request.module.__name__)}.s3"
    if load_class(target):
        print(f"Mocking {target}")
        client = mocker.MagicMock()
        client_func = mocker.patch(target)
        client_func.return_value = client
        return client


@pytest.fixture(scope="function")
def stack_params_and_outputs_and_stack(mocker, request):
    target = "{}.{}.stack_params_and_outputs_and_stack".format(
        BASE_MODULE_NAME, get_test_target_module(request.module.__name__)
    )
    if load_class(target):
        print(f"Mocking {target}")
        client_func = mocker.patch(target)
        return client_func


@pytest.fixture(scope="function")
def cloudfront_paginator(mocker, cloudfront):
    paginator = mocker.MagicMock()
    cloudfront.get_paginator.return_value = paginator
    return paginator


def load_class(name):
    components = name.split(".")
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod
