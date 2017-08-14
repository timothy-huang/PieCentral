# When all devices work, use $(notdir $(wildcard ../devices/*))
DEVICES := BatteryBuzzer ExampleDevice LimitSwitch LineFollower Potentiometer \
	RFID ServoControl TeamFlag YogiBear

.PHONY: install artifacts-install lint test $(DEVICES)

install:
	cd .. && wget https://downloads.arduino.cc/arduino-1.8.1-linux64.tar.xz
	cd .. && sudo bash setup.sh "arduino-1.8.1-linux64.tar.xz"
	pip3 install -r ../requirements.txt

artifacts-install:
	$(nop)

lint:
	cd .. && pylint *.py

unit_tests:
	cd .. && python3 -m unittest unit_tests/*.py

test: $(DEVICES) unit_tests

$(DEVICES):
	cd .. && rm -rf ./bin
	cd .. && make DEVICE=$@
