#!/bin/bash

#die Daten der benoetigten runs muessen hier in der folgenden Notation hinterlegt werden:
#01.08.24 13:50 --> 0108_1350
##run=" 2309_1916 2409_0716 2409_1600 2509_0000 2509_0800 2509_1600 "   #1800 MHz

##run=" 2609_0000 2609_0800 2609_1500 2609_2200 2709_0500 "             #2200 MHz

##run=" 2709_1200 2709_2200 2809_0800 2809_1800 2909_0400 "      #1400 MHz

#run=" 2909_1400 2909_2300 3009_1200 3009_2100 0210_1150 "     #1600 MHz

#run=" 0310_0000 0310_0800 0310_1600 0410_0000 0410_0800 0410_1600 "        #2000 MHz

#run=" 0510_0000 0510_0600 0510_1200 0510_1800 0710_1749 "        #2400 MHz

#run=' 0710_1010 '  attempt on 2600 MHz

#run=" 0810_1752 0910_1620 1010_0020 1010_0820 " #2400MHz, n vcores

#run=" 1010_1600 1110_0000 1110_1200 1210_0000 1210_1200 1310_1645 1310_2100 1410_0300 "

#run=" 1410_1800 1510_0000 1510_1200 "

#run=" 1610_1600 1710_1400 1710_2200 1810_1400 1810_2200 1910_0600 1910_1800 2010_0600 2010_1800 2110_0600 2110_1800 2210_0600 2210_1800 2310_0600 2310_1800 "

#run=" 2410_1900 2510_0700 2510_1900 2610_0700 2610_1900 2810_1900 2910_0700 "
#run=" 2910_1900 "

run=" 3010_0700 "

for j in $run
do
    mkdir ../../../03_input_data/run_$j

    mkdir ../../../03_input_data/run_$j/n4505
    mkdir ../../../03_input_data/run_$j/n4506
    mkdir ../../../03_input_data/run_$j/n4507
    mkdir ../../../03_input_data/run_$j/n4508
    
    scp lradmin@n4505.bfg.uni-freiburg.de:/adm/lradmin/data/run_$j/* ../../../03_input_data/run_$j/n4505/
    scp lradmin@n4506.bfg.uni-freiburg.de:/adm/lradmin/data/run_$j/* ../../../03_input_data/run_$j/n4506/
    scp lradmin@n4507.bfg.uni-freiburg.de:/adm/lradmin/data/run_$j/* ../../../03_input_data/run_$j/n4507/
    scp lradmin@n4508.bfg.uni-freiburg.de:/adm/lradmin/data/run_$j/* ../../../03_input_data/run_$j/n4508/
done

#scp lradmin@n4505.bfg.uni-freiburg.de:/adm/lradmin/data/hepscores_n4505.csv ../../04_output_data/
#scp lradmin@n4506.bfg.uni-freiburg.de:/adm/lradmin/data/hepscores_n4506.csv ../../04_output_data/
#scp lradmin@n4507.bfg.uni-freiburg.de:/adm/lradmin/data/hepscores_n4507.csv ../../04_output_data/
#scp lradmin@n4508.bfg.uni-freiburg.de:/adm/lradmin/data/hepscores_n4508.csv ../../04_output_data/
