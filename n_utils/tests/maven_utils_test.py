import xml.etree.ElementTree as ET
from subprocess import Popen

import pytest

from n_utils.maven_utils import add_server


@pytest.fixture(autouse=True)
def cleanup():
    yield
    proc = Popen(["git", "restore", "n_utils/tests/pom.xml"])
    _, _ = proc.communicate()


def test_add_server():
    pomfile = "n_utils/tests/pom.xml"
    add_server(pomfile, "deploy", "deployer")
    tree = ET.parse(pomfile)
    settings = tree.getroot()
    servers = settings.find("./servers")
    deployer_server = servers.find("./server[id='deploy']")
    assert deployer_server
    password = deployer_server.find("./password")
    username_el = deployer_server.find("./username")
    assert password.text == "password"
    assert username_el.text == "deployer"
