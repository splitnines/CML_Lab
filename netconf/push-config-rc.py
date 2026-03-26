import json
import sys
from urllib.parse import quote

import requests
import urllib3
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning


def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def main() -> None:
    host = sys.argv[1]
    username = "cisco"
    password = "cisco"
    verify_tls = False

    if not host:
        die("Set ROUTER_HOST.")

    if len(sys.argv) != 3:
        die(f"Usage: {sys.argv[0]} [hosname/IP] [DESCRIPTION]")

    description = sys.argv[2]

    iface_key = "1"
    iface_key_encoded = quote(iface_key, safe="")

    if not verify_tls:
        urllib3.disable_warnings(category=InsecureRequestWarning)

    url = (
        f"https://{host}/restconf/data/"
        f"Cisco-IOS-XE-native:native/interface/GigabitEthernet={iface_key_encoded}"
    )

    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }

    payload = {
        "Cisco-IOS-XE-native:GigabitEthernet": {
            "name": iface_key,
            "description": description,
        }
    }

    try:
        response = requests.patch(
            url,
            headers=headers,
            auth=HTTPBasicAuth(username, password),
            json=payload,
            verify=verify_tls,
            timeout=5,
        )
    except requests.RequestException as e:
        die(f"Request failed: {e}")

    if response.status_code not in (200, 201, 204):
        die(f"PATCH failed with HTTP {response.status_code}\n{response.text}")

    print("Interface description updated successfully.")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
