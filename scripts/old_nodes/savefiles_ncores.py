from subprocess import run
from tools import *
import sys

### writes a .csv file with hepscore of the run, the run, and the clock-freq
### also saves the .log and .json file in an run-specific folder


def get_loc(result):
    '''ruft aus einer einer uebergebenen Variable den filepath der Dokumentationdateien ab'''
    return result.split()[-2]


def get_hepscore(result):
    '''ruft aus einer uebergebenen Variable den HEPScore ab'''
    return result.split()[-28]


def copy_files(result):
    '''kopiert die Dokumentationfiles eines HEP-runs in den Datenordner des runs'''

    time = get_runname()
    #print(name)
    loc = get_loc(result=result).split('/')
    for i in ['run_config.yaml', 'hep-benchmark-suite.log', 'bmkrun_report.json']:
        loc[-1] = i
        file = "/".join(loc)
        run([f'cp {file} /adm/lradmin/data/run_{time}'], shell=True, capture_output = True, text = True)


def main(cores, result):
    '''speichert den HEPScore in der .csv Datei'''

    try:
        hostname = get_hostname()
    except Exception as err:
        f = open('/adm/lradmin/data/errorlog.txt', 'a')
        f.write(f"\nUnexpected {err=}, {type(err)=} (bei get_hostname())")
        f.close()

    try:
        runtime = get_runname()
    except Exception as err:
        f = open('/adm/lradmin/data/errorlog.txt', 'a')
        f.write(f"\nUnexpected {err=}, {type(err)=} (bei get_runname())")
        f.close()
    
    measurement = f'run_{runtime}'
    
    try:
        hepscore = get_hepscore(result=result)
    except Exception as err:
        f = open('/adm/lradmin/data/errorlog.txt', 'a')
        f.write(f"\nUnexpected {err=}, {type(err)=} (bei get_hepscore(result))")
        f.close()
    
    speed = get_speed().split(',')[0]
    
    f = open(f"/adm/lradmin/data/hepscores_{hostname}.csv", "a")
    f.write(f"\n{measurement},{hepscore},{speed},{cores}")
    f.close()



if __name__ == "__main__":
    cores = sys.argv[1]
    result = sys.argv[2]

    try:
        copy_files(result)
    except Exception as err:
        f = open('/adm/lradmin/data/errorlog.txt', 'a')
        f.write(f"\nUnexpected {err=}, {type(err)=} (bei copy_files)")
        f.close()
        
    main(cores, result)    
