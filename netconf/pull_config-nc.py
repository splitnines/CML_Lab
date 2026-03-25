from __future__ import annotations

import argparse
import sys
# from pathlib import Path

from ncclient import manager
from ncclient.operations import RPCError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pull running configuration from a Cisco IOS-XE router "
        "via NETCONF."
    )
    parser.add_argument(
        "--host", required=True, help="Router IP address or hostname"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=830,
        help="NETCONF SSH port (default: 830)",
    )
    parser.add_argument("--username", required=True, help="Username")
    parser.add_argument("--password", required=True, help="Password")
    parser.add_argument(
        "--output",
        default="running-config.xml",
        help="Output file path (default: running-config.xml)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="NETCONF session timeout in seconds (default: 30)",
    )
    parser.add_argument(
        "--hostkey-verify",
        action="store_true",
        help="Enable SSH host key verification",
    )
    return parser.parse_args()


def get_running_config(
    host: str,
    port: int,
    username: str,
    password: str,
    timeout: int,
    hostkey_verify: bool,
) -> str:
    with manager.connect(
        host=host,
        port=port,
        username=username,
        password=password,
        hostkey_verify=hostkey_verify,
        device_params={"name": "iosxe"},
        timeout=timeout,
        allow_agent=False,
        look_for_keys=False,
    ) as session:
        reply = session.get_config(source="running")
        return reply.data_xml


def main() -> int:
    args = parse_args()
    # output_path = Path(args.output)

    try:
        config_xml = get_running_config(
            host=args.host,
            port=args.port,
            username=args.username,
            password=args.password,
            timeout=args.timeout,
            hostkey_verify=args.hostkey_verify,
        )
    except RPCError as exc:
        print(f"NETCONF RPC failed: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Connection failed: {exc}", file=sys.stderr)
        return 1

    # output_path.write_text(config_xml, encoding="utf-8")
    print(config_xml)
    # print(f"Saved running config XML to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
