from tools import *
from subprocess import run

### da einige scheduled runs gemacht wurden bevor die Dateien automatisch gespeichert wurden,
### muss dieses skript einmal "manuell" geschrieben und ausgefuhrt werden

result = run(['cat /adm/lradmin/data/hepscores.txt'], shell=True, capture_output = True, text = True)
result = result.stdout.split('#')


name = get_hostname()
f = open(f"/adm/lradmin/data/hepscores_{name}.csv", "w")
f.write(f"run_{name}, hepscore_{name}, speed_{name}")
f.close()

def get_hepscore(file: str):
    '''ruft aus einer .txt Datei mit den HEPScore-Ergebnissen den HEPScore ab'''

    #result = run(['cat /adm/lradmin/data/hepscores.txt'], shell=True, capture_output = True, text = True)
    return file.split()[-27]

def get_loc(file: str):
    return file.split()[-2]


for i in [['run_2109_0610', 4], ['run_2109_1810', 6], ['run_2209_0610', 8], ['run_2209_1810', 10], ['run_2309_0610', 12]]:
    measurement = i[0]
    hepscore = get_hepscore(result[i[1]])

    f = open(f"/adm/lradmin/data/hepscores_{name}.csv", "a")
    f.write(f"\n{measurement},{hepscore},1200000")
    f.close()


for i in [['2109_0610', 4], ['2109_1810', 6], ['2209_0610', 8], ['2209_1810', 10], ['2309_0610', 12]]:
    time = i[0]
    #print(name)
    loc = get_loc(result[i[1]]).split('/')
    for i in ['run_config.yaml', 'hep-benchmark-suite.log', 'bmkrun_report.json']:
        loc[-1] = i
        file = "/".join(loc)
        run([f'cp {file} /adm/lradmin/data/run_{time}'], shell=True, capture_output = True, text = True)
