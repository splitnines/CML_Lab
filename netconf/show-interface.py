from ncclient import manager

router = "10.0.0.248"
username = "cisco"
password = "cisco"

filter_xml = """
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <interface>
    <GigabitEthernet>
      <name>1</name>
    </GigabitEthernet>
  </interface>
</native>
"""

with manager.connect(
    host=router,
    port=830,
    username=username,
    password=password,
    hostkey_verify=False,
    device_params={"name": "iosxe"},
    timeout=30,
) as m:
    reply = m.get_config(source="running", filter=("subtree", filter_xml))
    print(reply.xml)
