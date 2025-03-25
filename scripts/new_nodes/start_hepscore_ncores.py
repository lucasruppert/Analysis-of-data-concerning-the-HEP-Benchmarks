from subprocess import run
from time import sleep
import sys

def get_load():
    '''executes "uptime" and returns the current system-load as a float'''

    result = run(["uptime"], shell = True, capture_output = True, text = True)
    if result.returncode == 0:
        load = float(result.stdout.split()[-3].removesuffix(',').replace(',', '.'))
        return load
    
    else:
        return None



def main():
    reps = 20       ## this is the number of times the for loop below is executed
                    ## it ensures that no other processes run on the server to prevent overloading

    k = 0
    for i in range(reps):
        load = get_load()
        if load < 3:
            k += 1
        
        sleep(30)


    if k == reps:

        freq = sys.argv[1]
        cores = sys.argv[2]

        if str(freq) != 'default':
            try:
                run([f'/adm/lradmin/code/change_freq.sh {freq}'], shell=True, capture_output = True, text = True)
            except Exception as err:
                f = open('/adm/lradmin/data/errorlog.txt', 'a')
                f.write(f"\nUnexpected {err=}, {type(err)=} (bei change_freq.sh)")
                f.close()


        result = run([f'bmkrun -c /tmp/hep-ncores-config/ncores_{cores}/workdir/bmkrun_config.yml'], shell=True, capture_output = True, text = True)

        try:
            run([f'python3 /adm/lradmin/code/savefiles_ncores.py {cores} {result.stdout}'], shell=True, capture_output = True, text = True)
        except Exception as err:
            f = open('/adm/lradmin/data/errorlog.txt', 'a')
            f.write(f"\nUnexpected {err=}, {type(err)=} (bei savefiles_ncores.py)")
            f.close()

        print(result.stdout)

    else:
        print('Fehler: load zu hoch, HEPScore wird NICHT gestartet.')


if __name__ == "__main__":
    main()
