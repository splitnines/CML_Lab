#!/usr/bin/env python3

import json
import os
import sys
from urllib.parse import quote

import requests
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning


def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def main() -> None:
    host = os.environ.get("ROUTER_HOST", sys.argv[1])
    username = os.environ.get("ROUTER_USERNAME", "cisco")
    password = os.environ.get("ROUTER_PASSWORD", "cisco")
    verify_tls = os.environ.get("ROUTER_VERIFY_TLS", "false").lower() in {
        "1",
        "true",
        "yes",
    }

    if not host or not username or not password:
        die(
            "Set ROUTER_HOST, ROUTER_USERNAME, and ROUTER_PASSWORD in the environment."
        )

    if len(sys.argv) != 3:
        die(f"Usage: {sys.argv[0]} 'DESCRIPTION'")

    description = sys.argv[2]

    # User asked for gig1 -> treat that as GigabitEthernet1
    iface_key = "1"
    iface_key_encoded = quote(iface_key, safe="")

    if not verify_tls:
        requests.packages.urllib3.disable_warnings(
            category=InsecureRequestWarning
        )

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
            timeout=30,
        )
    except requests.RequestException as exc:
        die(f"Request failed: {exc}")

    if response.status_code not in (200, 201, 204):
        die(f"PATCH failed with HTTP {response.status_code}\n{response.text}")

    print("Interface description updated successfully.")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
