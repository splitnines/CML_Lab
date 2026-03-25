from ncclient import manager

config = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <GigabitEthernet>
        <name>1</name>
        <description>Uplink to core</description>
      </GigabitEthernet>
    </interface>
  </native>
</config>
"""

with manager.connect(
    host="10.0.0.248",
    port=830,
    username="cisco",
    password="cisco",
    hostkey_verify=False,
    device_params={"name": "iosxe"},
    timeout=5,
) as m:
    reply = m.edit_config(target="running", config=config)
    print(reply.xml)
