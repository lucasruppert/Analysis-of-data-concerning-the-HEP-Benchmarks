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
    result = result.split('#')[-1]

    time = get_runname()
    copy_files(result, time)

    hostname = get_hostname()
    runtime = get_runname()
    measurement = f'run_{runtime}'
    hepscore = get_hepscore(result)
    freq = sys.argv[1]
    ncores = sys.argv[2]
    
    f = open(f"/adm/lradmin/data/hepscores_{hostname}.csv", "a")
    f.write(f"\n{measurement},{hostname},{hepscore},{freq},{ncores}")
    f.close()


def copy_all_runs():

    with open('/adm/lradmin/data/hepscores_ncores.txt', 'r') as f:
        result = f.read() 
    result = result.split('#')

    for i in [['1610_1600', 32], ['1710_1400', 34], ['1710_2200', 36], ['1810_1400', 38], ['1810_2200', 40], ['1910_0600', 42], ['1910_1800', 44], ['2010_0600', 46],
              ['2010_1800', 48], ['2110_0600', 50]]:
        #[['1510_1200', 30]]
        #[['1410_1800', 26], ['1510_0000', 28]]
        #[['1010_1600', 10], ['1110_0000', 12], ['1110_1200', 14], ['1210_0000', 16], ['1310_1645', 20], ['1310_2100', 22], ['1410_0300', 24]]
        #[['0810_1752', 2], ['0910_1620', 4], ['1010_0020', 6], ['1010_0820', 8]]:
        copy_files(result[i[1]], i[0])

if __name__ == "__main__":
    main()