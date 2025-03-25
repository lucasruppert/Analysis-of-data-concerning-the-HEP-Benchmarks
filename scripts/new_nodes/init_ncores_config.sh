#!/bin/bash

cd /tmp

git clone https://gitlab.cern.ch/hep-benchmarks/hep-benchmark-suite.git

mkdir /tmp/hep-ncores-config
#Cores=" 8 16 32 48 96 128 160 192 196 200 224 240 256 "

#for cores in $Cores
#do
#    mkdir /tmp/hep-ncores-config/ncores_$cores
#    cd /tmp/hep-ncores-config/ncores_$cores
#    /tmp/hep-benchmark-suite/examples/hepscore/run_HEPscore_configurable_ncores.sh -n $cores
#done
cores=$(nproc --all)
i=4

while [[ $i -le $cores ]]; do
  mkdir /tmp/hep-ncores-config/ncores_$i
  cd /tmp/hep-ncores-config/ncores_$i
  /tmp/hep-benchmark-suite/examples/hepscore/run_HEPscore_configurable_ncores.sh -n $i
  ((i += 4))
done
