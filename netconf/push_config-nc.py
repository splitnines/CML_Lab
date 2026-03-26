from ncclient import manager
import sys

with open(sys.argv[2], "r") as xml:
    config = xml.read()

with manager.connect(
    host=sys.argv[1],
    port=830,
    username="cisco",
    password="cisco",
    hostkey_verify=False,
    device_params={"name": "iosxe"},
    timeout=5,
) as m:
    reply = m.edit_config(target="running", config=config)
    print(reply.xml)
