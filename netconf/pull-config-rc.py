#!/usr/bin/env python3

import json
import os
import sys

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

    if not verify_tls:
        requests.packages.urllib3.disable_warnings(
            category=InsecureRequestWarning
        )

    url = f"https://{host}/restconf/data/Cisco-IOS-XE-native:native"
    headers = {
        "Accept": "application/yang-data+json",
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            auth=HTTPBasicAuth(username, password),
            verify=verify_tls,
            timeout=30,
        )
    except requests.RequestException as exc:
        die(f"Request failed: {exc}")

    if not response.ok:
        die(f"HTTP {response.status_code}\n{response.text}")

    try:
        data = response.json()
    except ValueError:
        die("Device did not return valid JSON.")

    print(json.dumps(data, indent=2, sort_keys=False))


if __name__ == "__main__":
    main()
