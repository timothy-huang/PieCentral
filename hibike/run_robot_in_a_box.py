#!/usr/bin/env python3
"""
Fetch code from a branch of PieCentral, then run hardware tests to verify
that it works.

Author: Brose Johnstone
"""
import os
import argparse
import subprocess

import hibike_process, hibike_message as hm


def shell_script(text):
    """
    Execute each line of TEXT as a shell command.
    If any command fails, an exception is thrown.
    """
    for line in text:
        subprocess.check_call(line, shell=True)


parser = argparse.ArgumentParser(description="Fetch code from a PieCentral branch and run tests on it.")
parser.add_argument("branch", help="The branch to fetch code from")
args = parser.parse_args()

shell_script("""
sudo systemctl stop runtime.service
cd ~
""")
if not os.path.exists("PieCentral"):
    shell_script("git clone https://github.com/pioneers/PieCentral")

print("Checking in branch")
shell_script("""
cd PieCentral
git checkout origin/{0}
git fetch origin
git reset --hard origin/{0}
""".format(args.branch))
print("Making Arduino modules")
shell_script("""
cd hibike/travis
make test
""")
# Once we are done compiling, check connected sensors and their types.
# Uncomment these lines once branch merges
from hibike_process import get_working_serial_ports, identify_smart_sensors
ports = get_working_serial_ports()
sensors = identify_smart_sensors(ports)
sensor_types = {k: hm.devices[hm.getDeviceType(v)] for (k, v) in sensors.items()}
for (k, v) in sensor_types.items():
   shell_script("make MONITOR_PORT={} DEVICE={}".format(k, v))
