from subprocess import run
from tools import get_runname, get_hostname
import sys


def get_loc(result):
    '''ruft aus einer einer uebergebenen Variable den filepath der Dokumentationdateien ab'''
    return result.split()[-2]


def get_hepscore(result):
    '''ruft aus einer uebergebenen Variable den HEPScore ab'''
    return result.split()[-28]


def copy_files(result, time):
    '''kopiert die Dokumentationfiles eines HEP-runs in den Datenordner des runs'''

    loc = get_loc(result=result).split('/')
    for i in ['run_config.yaml', 'hep-benchmark-suite.log', 'bmkrun_report.json']:
        loc[-1] = i
        file = "/".join(loc)
        output = run([f'cp {file} /adm/lradmin/data/run_{time}'], shell=True, capture_output = True, text = True)
        f = open('error.txt', 'a')
        f.write(f'{output}\n')
        f.close()


def main():
    with open('/adm/lradmin/data/hepscores_ncores.txt', 'r') as f:
        result = f.read() 
    result = result.split('#')

    time = get_runname()
    copy_files(result[-1], time)

    hostname = get_hostname()
    runtime = get_runname()
    measurement = f'run_{runtime}'
    hepscore = get_hepscore(result[-1])
    freq = sys.argv[1]
    ncores = sys.argv[2]
    
    f = open(f"/adm/lradmin/data/hepscores_{hostname}.csv", "a")
    f.write(f"\n{measurement},{hostname},{hepscore},{freq},{ncores}")
    f.close()


if __name__ == "__main__":
    main()