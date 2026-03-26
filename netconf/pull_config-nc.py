from __future__ import annotations

import sys

from ncclient import manager
from ncclient.operations import RPCError
from xml.etree import ElementTree as ET
from xml.dom import minidom


def get_running_config(
    host: str,
) -> str:
    with manager.connect(
        host=host,
        port=830,
        username="cisco",
        password="cisco",
        hostkey_verify=False,
        device_params={"name": "iosxe"},
        timeout=5,
        allow_agent=False,
        look_for_keys=False,
    ) as session:
        reply = session.get_config(source="running")
        return reply.data_xml


def main() -> int:
    try:
        config_xml = get_running_config(host=sys.argv[1])
    except RPCError as e:
        print(f"NETCONF RPC failed: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Connection failed: {e}", file=sys.stderr)
        return 1

    root = ET.fromstring(config_xml)
    rough = ET.tostring(root, encoding="utf-8")
    pretty = minidom.parseString(rough).toprettyxml(indent="  ")
    print(pretty)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
