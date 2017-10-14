#!/bin/bash

#make sure to install zip command using sudo apt install.. 

mkdir temp && cd temp

journalctl -e -u update.service > update.log
journalctl -e -u runtime.service > service.log
journalctl -e -u networking.service > networking.log

cd $HOME 




