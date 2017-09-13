from hibike_tester.py import Hibike
import hibike_message.py as hm
import time

yogibear= [	HIBIKE.make_send_write(dev_uid, [("duty_cycle", 0)]),
	    	HIBIKE.make_send_write(dev_uid, [("duty_cycle", 0.5)]),
	    	HIBIKE.make_send_write(dev_uid, [("duty_cycle", 1.0)]),
	    	HIBIKE.make_send_write(dev_uid, [("duty_cycle", 0)]),
	    	HIBIKE.make_send_write(dev_uid, [("duty_cycle", -0.5)]),
	    	HIBIKE.make_send_write(dev_uid, [("duty_cycle", -1.0)]),
	    	HIBIKE.make_send_write(dev_uid, [("duty_cycle", 0)])]
commands={"YogiBear":(yogibear,0.75)}

HIBIKE=Hibike()
HIBIKE.run_commands(commands)
