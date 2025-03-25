#!/bin/bash

MYENV="bmk_env"
source /adm/lradmin/$MYENV/bin/activate
run=$(python3 /adm/lradmin/hepscore_start.py)
echo $run >> /adm/lradmin/data/hepscores.txt
python3 /adm/lradmin/code/write_hepscore.py