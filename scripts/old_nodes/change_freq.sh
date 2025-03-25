#!/bin/bash

sudo cpupower frequency-set -d $1
sudo cpupower frequency-set -u $1
sudo cpupower frequency-set -f $1