import os
import sys
import termios

from pyats.topology import loader


fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

testbed = loader.load("testbed.yaml")

try:
    if os.isatty(fd) and hasattr(termios, "ECHOCTL"):
        new_settiings = termios.tcgetattr(fd)
        new_settiings[3] &= ~termios.ECHOCTL
        termios.tcsetattr(fd, termios.TCSANOW, new_settiings)

    print("Initializing connections to testbed devices...", end="", flush=True)

    testbed.connect(log_stdout=False)

    print("complete!")

    for device in testbed.devices.values():
        print(f"--- {device.name} ---")
        eigrp_ints = device.parse("show ip eigrp interfaces")["vrf"][
            "default"
        ]["eigrp_instance"]

        for asn, eigrp_int in eigrp_ints.items():
            interfaces = eigrp_int["address_family"]["ipv4"]["interface"]
            for interface_name, metrics in interfaces.items():
                if metrics["peers"] < 1:
                    print(asn, interface_name, metrics["peers"], "no peers")
                else:
                    print(asn, interface_name, metrics["peers"])


except KeyboardInterrupt:
    pass
finally:
    print("\nDisconnecting from devices...", end="", flush=True)
    testbed.disconnect()
    termios.tcsetattr(fd, termios.TCSANOW, old_settings)
    print("done.")
