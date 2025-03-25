from subprocess import run
from tools import *

### writes a .csv file with hepscore of the run, the run, and the clock-freq
### also saves the .log and .json file in an run-specific folder

def get_loc():
    '''ruft aus einer .txt Datei mit den HEPScore-Ergebnissen den filepath der Dokumentationdateien ab'''

    result = run(['cat /adm/lradmin/data/hepscores.txt'], shell=True, capture_output = True, text = True)
    return result.stdout.split()[-2]


def get_hepscore():
    '''ruft aus einer .txt Datei mit den HEPScore-Ergebnissen den HEPScore ab'''

    result = run(['cat /adm/lradmin/data/hepscores.txt'], shell=True, capture_output = True, text = True)
    return result.stdout.split()[-27]


def copy_files():
    '''kopiert die Dokumentationfiles eines HEP-runs in den Datenordner des runs'''

    time = get_runname()
    #print(name)
    loc = get_loc().split('/')
    for i in ['run_config.yaml', 'hep-benchmark-suite.log', 'bmkrun_report.json']:
        loc[-1] = i
        file = "/".join(loc)
        run([f'cp {file} /adm/lradmin/data/run_{time}'], shell=True, capture_output = True, text = True)


def main():
    '''speichert den HEPScore in der .csv Datei'''

    hostname = get_hostname()
    runtime = get_runname()
    measurement = f'run_{runtime}'
    hepscore = get_hepscore()
    speed = get_speed().split(',')[0]
    
    f = open(f"/adm/lradmin/data/hepscores_{hostname}.csv", "a")
    f.write(f"\n{measurement},{hepscore},{speed}")
    f.close()



if __name__ == "__main__":
    main()
    copy_files()
