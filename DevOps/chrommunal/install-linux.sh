#!/bin/sh

#enable legacy boot
sudo crossystem dev_boot_usb=1 dev_boot_legacy=1

#flash firmware
cd; curl -LO https://mrchromebox.tech/firmware-util.sh && sudo bash firmware-util.sh


