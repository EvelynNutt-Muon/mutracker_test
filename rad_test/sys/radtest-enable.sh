#!/bin/bash

# Mostly a one time thing but included to ensure the latest service is used.
cp /home/pi/mutracker_test/rad_test/sys/radtest.service /lib/systemd/system

# Enable and start the radtest service.
systemctl enable radtest.service
systemctl start radtest.service