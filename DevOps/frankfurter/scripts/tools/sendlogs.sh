#!/bin/bash

mkdir temp && cd temp

journalctl -e -u update.service > update.log
journalctl -e -u runtime.service > service.log
journalctl -e -u network.service > network.log


