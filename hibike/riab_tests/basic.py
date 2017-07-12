import unittest
from hibike_tester import Hibike
from hibike_process import identify_smart_sensors, get_working_serial_ports
import hibike_message as hm
from run_robot_in_a_box import get_sensor_types

class BasicTests(unittest.TestCase):
    EXPECTED_SENSORS = {"/dev/ttyACM0": "ServoControl",
                        "/dev/ttyACM2": "YogiBear",
                        "/dev/ttyACM1": "RFID",
                        "/dev/ttyACM3": "LimitSwitch"}
    @classmethod
    def setUpClass(cls):
        from run_robot_in_a_box import stop_runtime
        stop_runtime()

    @classmethod 
    def tearDownClass(cls):
        from run_robot_in_a_box import start_runtime
        start_runtime()

    def test_list_devices(self):
        """
        Check that the expected devices enumerate.
        """
        sensors = get_sensor_types()
        self.assertEqual(self.EXPECTED_SENSORS, sensors)
    
    def test_subscribe(self):
        """
        Subscribe to some devices and see what happens.
        """
        serials, _ = get_working_serial_ports()
        sensors = identify_smart_sensors(serials)
        del serials

        process = Hibike()
        for uid in sensors.values():
            # Shut up sensors
            process.subscribe(uid, 0, [])
        for uid in sensors.values():
            device_id = hm.uid_to_device_id(uid)
            params = hm.all_params_for_device_id(device_id)
            process.subscribe(uid, 1, params)
        # We should be receiving data
        while True:
            packet = process.state_queue.get()
            if packet[0] == "device_values":
                for uid in sensors.values():
                    self.assertIn(uid, packet[1][0])

if __name__ == "__main__":
    unittest.main()