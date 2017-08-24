from hibike_tester.py import Hibike
import hibike_message.py as hm
import time

HIBIKE = Hibike()
HIBIKE.enumerate()
while True:
	command,main_args=HIBIKE.state_queue.get()
	if command == "device_subscribed":
		# At the beginning of the script, set prescribed actions to run continuously in intervals
		dev_uid - main_args[0]
		if dev_uid not in uids:
			uids.add(dev_uid)
			if HIBIKE.sensor_type(dev_uid) == "YogiBear":
	            HIBIKE.set_interval_sequence([
	                HIBIKE.make_send_write(dev_uid, [("duty_cycle", 0)]),
	                HIBIKE.make_send_write(dev_uid, [("duty_cycle", 0.5)]),
	                HIBIKE.make_send_write(dev_uid, [("duty_cycle", 1.0)]),
	                HIBIKE.make_send_write(dev_uid, [("duty_cycle", 0)]),
	                HIBIKE.make_send_write(dev_uid, [("duty_cycle", -0.5)]),
	                HIBIKE.make_send_write(dev_uid, [("duty_cycle", -1.0)]),
	                HIBIKE.make_send_write(dev_uid, [("duty_cycle", 0)])
	                ], 0.75)
            parameters = []
            for param in hm.DEVICES[hm.uid_to_device_id(dev_uid)]["params"]:
                parameters.append(param["name"])
            HIBIKE.pipe_to_child.send(["subscribe_device", [dev_uid, 10, parameters]])
    elif command == "device_values":
        print("%10.2f, %s" % (time.time(), str(main_args)))