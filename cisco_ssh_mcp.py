from __future__ import annotations

import os
from dataclasses import dataclass

from fastmcp import FastMCP
from netmiko import ConnectHandler

mcp = FastMCP("Cisco SSH")


@dataclass
class CiscoCommandResult:
    command: str
    output: str


def _normalize(cmd: str) -> str:
    return " ".join(cmd.strip().split())


def _connect(host: str):
    h = host.strip()
    if not h:
        msg = "host is required"
        raise ValueError(msg)

    username = os.environ["IXC_USERNAME"]
    password = os.environ["IXC_PASSWORD"]
    device_type = "cisco_ios"
    secret = ""

    conn = ConnectHandler(
        device_type=device_type,
        host=h,
        username=username,
        password=password,
        secret=secret,
        use_keys=False,
        timeout=10,
        banner_timeout=10,
        auth_timeout=10,
    )

    if secret:
        conn.enable()

    return conn


@mcp.tool
def cisco_command(host: str, command: str) -> CiscoCommandResult:
    cmd = _normalize(command)
    if not cmd:
        msg = "command is required"
        raise ValueError(msg)

    conn = _connect(host)
    try:
        output = conn.send_command(
            cmd,
            strip_prompt=False,
            strip_command=False,
        )
        return CiscoCommandResult(command=cmd, output=str(output))
    finally:
        conn.disconnect()


@mcp.tool
def cisco_command_many(
    host: str, commands: list[str]
) -> list[CiscoCommandResult]:
    cmds = [_normalize(command) for command in commands]
    if any(not command for command in cmds):
        msg = "commands must not contain empty entries"
        raise ValueError(msg)

    conn = _connect(host)
    try:
        results: list[CiscoCommandResult] = []
        for cmd in cmds:
            output = conn.send_command(
                cmd,
                strip_prompt=False,
                strip_command=False,
            )
            results.append(CiscoCommandResult(command=cmd, output=str(output)))
        return results
    finally:
        conn.disconnect()


if __name__ == "__main__":
    mcp.run()
