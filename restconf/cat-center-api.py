from catalystcentersdk import api
import json

cat = api.CatalystCenterAPI(
    username="devnetuser",
    password="Cisco123!",
    base_url="https://sandboxdnac.cisco.com",
    version="3.1.3.0",
    verify=False,
)

devices = cat.devices.get_device_list()

print(json.dumps(devices, indent=2))

# for device in devices.response:
#     print(device.hostname)
