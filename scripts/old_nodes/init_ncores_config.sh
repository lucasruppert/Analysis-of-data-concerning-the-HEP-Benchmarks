#!/bin/bash

#cd /adm/lradmin

#git clone https://gitlab.cern.ch/hep-benchmarks/hep-benchmark-suite.git

#mkdir code
#mkdir data

mkdir /adm/lradmin/hep-ncores-config
Cores=" 84 100 116 132 148 164 180 196 212 228 "

for cores in $Cores
do
    mkdir /adm/lradmin/hep-ncores-config/ncores_$cores
    cd /adm/lradmin/hep-ncores-config/ncores_$cores
    /adm/lradmin/hep-benchmark-suite/examples/hepscore/run_HEPscore_configurable_ncores.sh -n $cores
done

cd /adm/lradmin

#export MYENV="bmk_env"        # Define the name of the environment.
#python3 -m venv $MYENV        # Create a directory with the virtual environment.
#source $MYENV/bin/activate    # Activate the environment.
#python3 -m pip install git+https://gitlab.cern.ch/hep-benchmarks/hep-benchmark-suite.git