#!/bin/bash

jobs_to_run=`head -n1 /adm/lradmin/data/jobs_to_run.txt`

while [ "$jobs_to_run" != "end" ]
do
    echo start > /adm/lradmin/data/start_stop.txt
    sleep 100 #300

    MYENV="bmk_env"
    source /adm/lradmin/$MYENV/bin/activate
    run=$(python3 /adm/lradmin/start_hepscore_ncores.py)
    echo $run >> /adm/lradmin/data/hepscores_ncores.txt
    #echo "stop" > /adm/lradmin/data/start_stop.txt
    #python3 /adm/lradmin/code/write_hepscore.py

    sleep 300
    echo stop > /adm/lradmin/data/start_stop.txt

    jobs_to_run=`head -n1 /adm/lradmin/data/jobs_to_run.txt`
done

sleep 60
echo end > /adm/lradmin/data/start_stop.txt