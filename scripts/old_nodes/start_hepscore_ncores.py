from subprocess import run
from time import sleep
import sys

def get_load():
    '''fuehrt "uptime" aus und gibt den aktuellen system-load als float aus'''

    result = run(["uptime"], shell = True, capture_output = True, text = True)
    if result.returncode == 0:
        load = float(result.stdout.split()[-3].removesuffix(',').replace(',', '.'))
        return load
    
    else:
        return None



def main():
    reps = 20       ## hier sollen die Anzahl der Wiederholungen der untenstehenden Schleife angegeben werden

    k = 0
    for i in range(reps):
        load = get_load()
        if load < 3:
            k += 1
        
        sleep(30)


    if k == reps:
        ## der folgende Block holt die zu verwendende Frequenz und Cores aus einer txt-Datei und streicht den Job
        #with open('/adm/lradmin/data/jobs_to_run.txt', 'r') as f:
        #    jobs_to_run = f.read()
        
        #jobs_to_run = jobs_to_run.split('\n')
        #next_run = jobs_to_run[0].split(',')

        freq = sys.argv[1]         #next_run[0]
        cores = sys.argv[2]        #next_run[1]
        #count =         #int(next_run[2])

        #if count == 1:
        #    jobs_to_run.pop(0)
        #else:
        #    next_run[2] = str((count - 1))
        #    jobs_to_run[0] = ",".join(next_run)     

        #f = open('/adm/lradmin/data/jobs_to_run.txt', 'w')
        #f.write("\n".join(jobs_to_run))
        #f.close()

        if str(freq) != 'default':
            try:
                run([f'/adm/lradmin/code/change_freq.sh {freq}'], shell=True, capture_output = True, text = True)
            except Exception as err:
                f = open('/adm/lradmin/data/errorlog.txt', 'a')
                f.write(f"\nUnexpected {err=}, {type(err)=} (bei change_freq.sh)")
                f.close()


        result = run([f'bmkrun -c /adm/lradmin/hep-ncores-config/ncores_{cores}/workdir/bmkrun_config.yml'], shell=True, capture_output = True, text = True)

        try:
            run([f'python3 /adm/lradmin/code/savefiles_ncores.py {cores} {result.stdout}'], shell=True, capture_output = True, text = True)
        except Exception as err:
            f = open('/adm/lradmin/data/errorlog.txt', 'a')
            f.write(f"\nUnexpected {err=}, {type(err)=} (bei savefiles_ncores.py)")
            f.close()

        print(result.stdout)
        #print(f'\nworks: {freq},{cores},{count}')

    else:
        print('Fehler: load zu hoch, HEPScore wird NICHT gestartet.')


if __name__ == "__main__":
    main()
