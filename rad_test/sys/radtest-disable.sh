#!/bin/bash

# Disable and stop the radtest service.
systemctl stop radtest.service
systemctl disable radtest.service