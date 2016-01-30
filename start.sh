#!/bin/bash
source `which virtualenvwrapper.sh`
workon inzbot
./inzbot.py &
deactivate
