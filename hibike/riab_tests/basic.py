"""
Tests for basic Hibike functionality: subscription, reads, and writes.
"""

import unittest
import time
from hibike_tester import Hibike
from hibike_process import identify_smart_sensors, get_working_serial_ports
import hibike_message as hm
from run_robot_in_a_box import get_sensor_types, get_sensor_uids

class BasicTests(unittest.TestCase):
    EXPECTED_SENSORS = {"ServoControl", "YogiBear", "RFID", "LimitSwitch"}
    # Check for all devices' UIDs until this many seconds.
    DEVICE_READ_TIMEOUT = 5
    @classmethod
    def setUpClass(cls):
        from run_robot_in_a_box import stop_runtime
        stop_runtime()

    def test_list_devices(self):
        """
        Check that the expected devices enumerate.
        """
        sensors = set(get_sensor_types().values())
        self.assertEqual(self.EXPECTED_SENSORS, sensors)

    def test_subscribe(self):
        """
        Subscribe to some devices and see what happens.
        """
        sensors = get_sensor_uids()
        uids = set(sensors.values())
        reads = {uid: False for uid in uids}

        process = Hibike()
        for uid in sensors.values():
            # Shut up sensors
            process.subscribe(uid, 0, [])
        for uid in sensors.values():
            device_id = hm.uid_to_device_id(uid)
            params = hm.all_params_for_device_id(device_id)
            process.subscribe(uid, 1, params)
        # We should be receiving data
        curr_time = time.time()
        loop_time = time.time()
        while loop_time - curr_time <= self.DEVICE_READ_TIMEOUT:
            packet = process.state_queue.get()
            if packet[0] == "device_values":
                for uid in sensors.values():
                    reads[uid] = True
            loop_time = time.time()

        for (uid, read) in reads.items():
            self.assertTrue(read,
                            "subbed but didn't receive packet from {}".format(uid))

        process.disable()
        process.terminate()


if __name__ == "__main__":
    unittest.main()
