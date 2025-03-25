#!/bin/bash

now=$(python3 /adm/lradmin/code/date.py)
mkdir /adm/lradmin/data/run_$now
cd /adm/lradmin/data/run_$now
echo $now > /adm/lradmin/data/run_names.txt
sudo python3 /adm/lradmin/code/measurement_ncores.py
