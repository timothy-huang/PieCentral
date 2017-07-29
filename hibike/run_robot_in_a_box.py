#!/usr/bin/env python3
"""
Fetch code from a branch of PieCentral, then run hardware tests to verify
that it works.

Author: Brose Johnstone
"""
import os
import argparse
import subprocess
import unittest
from typing import Dict

import hibike_message as hm
import riab_tests

TESTING_DIR = "/tmp"


def shell_script(text):
    """
    Execute each line of TEXT as a shell command.
    If any command fails, an exception is thrown.
    """
    for line in text.split("\n"):
        retcode = subprocess.call(line, shell=True)
        if retcode != 0:
            raise Exception("Command {} failed with retcode {}".format(line, retcode))


def get_cmdline_args():
    """
    Parse command line arguments and return them.
    """
    parser = argparse.ArgumentParser(description="Fetch code from a PieCentral\
                                                  branch and run tests on it.")
    parser.add_argument("branch", help="the branch to test")
    parser.add_argument("-f", "--flash-sensors", action="store_true",
                        help="flash sensors with code")
    return parser.parse_args()

def stop_runtime():
    """ Stop the runtime service. """
    shell_script("sudo systemctl stop runtime.service")


def start_runtime():
    """ Start the runtime service. """
    shell_script("sudo systemctl start runtime.service")


def check_in_branch(branch_name):
    """
    Check in the branch BRANCH_NAME of PieCentral.
    """
    shell_script("""
    git checkout origin/{0}
    git fetch origin
    git reset --hard origin/{0}
    """.format(branch_name))

def flash_sensors(type_dict: Dict[str, str]) -> None:
    """
    Flash sensors, where the keys of TYPE_DICT specify ports,
    and the values device types.
    """
    for (port, sensor_type) in type_dict.items():
        shell_script("make upload MONITOR_PORT={} DEVICE={}".format(port, sensor_type))


def compile_modules() -> None:
    """
    Compile all Hibike C++ files.

    This assumes we are in the travis directory already.
    """
    shell_script("make test")


def get_sensor_uids() -> Dict[str, int]:
    """
    Get a mapping from serial ports to device UIDs.

    This function should be used in place of identify_smart_sensors
    when the serial ports need to be used afterwards.
    """
    from hibike_process import get_working_serial_ports, identify_smart_sensors
    ports = get_working_serial_ports()[0]
    sensors = identify_smart_sensors(ports)
    for port in ports:
        port.close()
    return sensors


def get_sensor_types() -> Dict[str, str]:
    """
    Scan serial ports for working smart sensors and their types.

    Returns:
        A map from port names to sensor types.
    """
    sensors = get_sensor_uids()
    sensor_types = {k: hm.DEVICES[hm.get_device_type(v)]["name"] for (k, v) in sensors.items()}
    return sensor_types

def main():
    """
    Run robot in a box.
    """
    stop_runtime()
    args = get_cmdline_args()
    os.chdir(TESTING_DIR)
    if not os.path.exists(os.path.join(TESTING_DIR, "PieCentral")):
        shell_script("git clone https://github.com/pioneers/PieCentral")

    print("Checking in branch")
    os.chdir("PieCentral")
    check_in_branch(args.branch)
    # Check connected sensors and their types
    sensor_types = get_sensor_types()
    print(sensor_types)
    os.chdir("hibike")
    if args.flash_sensors:
        flash_sensors(sensor_types)

    from riab_tests import basic
    unittest.main(basic)


if __name__ == "__main__":
    main()
