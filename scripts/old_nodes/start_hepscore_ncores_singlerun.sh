#!/bin/bash

echo start > /adm/lradmin/data/start_stop.txt
sleep 100 #300

MYENV="bmk_env"
source /adm/lradmin/$MYENV/bin/activate
run=$(python3 /adm/lradmin/start_hepscore_ncores.py $1 $2)
echo $run >> /adm/lradmin/data/hepscores_ncores.txt
#echo "stop" > /adm/lradmin/data/start_stop.txt
#python3 /adm/lradmin/code/write_hepscore.py
python3 /adm/lradmin/code/copy_all_runs_ncores.py $1 $2

sleep 300
echo stop > /adm/lradmin/data/start_stop.txt