# Copyright 2017 Nitor Creations Oy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import xml.etree.ElementTree as ET


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def add_server(pomfile, server_id, username):
    tree = ET.parse(pomfile)
    settings = tree.getroot()
    servers = settings.find("./servers")
    if servers is None:
        servers = ET.SubElement(settings, "servers")
    deployer_server = servers.find("./server[id='" + server_id + "']")
    if deployer_server is None:
        deployer_server = ET.SubElement(servers, "server")
        ET.SubElement(deployer_server, "id").text = server_id
        ET.SubElement(deployer_server, "username")
    password = deployer_server.find("./password")
    username_el = deployer_server.find("./username")
    username_el.text = username
    if password is None:
        password = ET.SubElement(deployer_server, "password")
    password.text = os.getenv("DEPLOYER_PASSWORD", "password")
    indent(settings)
    tree.write(pomfile, encoding="utf-8")
