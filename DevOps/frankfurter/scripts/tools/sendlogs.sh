#!/bin/bash

#make sure to install zip command using sudo apt install.. 
#added zip pkg to master_frankfurter setup

mkdir temp && cd temp

#get the logs from these services and log them in temp directory
journalctl -e -u update.service > update.log
journalctl -e -u runtime.service > service.log
journalctl -e -u networking.service > networking.log

cd $HOME 

#zip log files and print out zip file if it was made
zip -r service-logs.zip temp && ls *.zip

#send files to host computer





