#!/bin/bash

sleep 60
start_stop=$(</adm/lradmin/data/start_stop.txt)

while [ "$start_stop" != "end" ]
do
    start_stop=$(</adm/lradmin/data/start_stop.txt)
    if [ "$start_stop" = "start" ]
    then
        now=$(python3 /adm/lradmin/code/date.py)
        mkdir /adm/lradmin/data/run_$now
        cd /adm/lradmin/data/run_$now
        echo $now > /adm/lradmin/data/run_names.txt
        sudo python3 /adm/lradmin/code/measurement_ncores.py
    fi
done
