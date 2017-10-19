#!/bin/bash

if [[ "$(id -u)" != "0" ]]; then
    echo "Please run with sudo permissions."
    exit 1
fi

install_if_absent () {
    if [[ "$(dpkg-query -W -f='${Status}' "$1" 2> /dev/null | grep -c "ok installed")" != 1 ]]; then
    	echo $1
        sudo apt-get --yes install "$1"
    fi
}

sudo cp utils/flash /etc/bash_completion.d/flash.sh
echo "Set up tab-complete"
echo "Please restart your terminals"

sudo usermod -a -G dialout "$(whoami)"

if [ $(ls /opt | grep -c "arduino-1.8.1") == 0 ]; then 
	curl "https://downloads.arduino.cc/arduino-1.8.1-linux64.tar.xz" | sudo tar -xJf - -C /opt
fi

deps=("make" "gcc" "gcc-avr" "arduino-mk" "python3-pip")
for dep in "${deps[@]}"; do
    install_if_absent $dep
done
