import json
import sys

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

    if not verify_tls:
        urllib3.disable_warnings(category=InsecureRequestWarning)

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
            timeout=5,
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
