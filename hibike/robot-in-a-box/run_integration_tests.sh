#!/bin/bash

# Fetch code from a branch of PieCentral, then run hardware and compile tests.
# Author: Brose Johnstone

function exit_with_msg {
	echo "$1"
	exit 1
}

if (( $# != 1 )) ; then
	echo "usage: $0 BRANCH_NAME"
	exit 1
fi


sudo systemctl stop runtime.service
cd ~
# Fetch branch from remote
if [ ! -e PieCentral ]; then
	git clone https://www.github.com/pioneers/PieCentral
fi

git checkout "$1" || exit_with_msg "Could not find branch"
git fetch origin
# Clean out any detritus left from previous runs
git reset --hard origin/"$1"
	
cd PieCentral
# Make all modules
cd hibike/travis/
make test || exit_with_msg "Failed to build Arduino modules"

echo "Flashing Arduinos"
# Flash all connected Arduinos
# TODO
# Once we are done flashing Arduinos, Hibike can step back in
sudo systemctl start runtime.service
sleep 5
echo "Generating test data"
# TODO
