from subprocess import run
from time import sleep

def get_load():
    '''fuehrt "uptime" aus und gibt den aktuellen system-load als float aus'''

    result = run(["uptime"], shell = True, capture_output = True, text = True)
    if result.returncode == 0:
        load = float(result.stdout.split()[-3].removesuffix(',').replace(',', '.'))
        return load
    
    else:
        return None


reps = 20       ## hier sollen die Anzahl der Wiederholungen der untenstehenden Schleife angegeben werden

k = 0
for i in range(reps):
    load = get_load()
    if load < 3:
        k += 1
    
    sleep(30)


if k == reps:
    result=run(['bmkrun -c default'], shell=True, capture_output = True, text = True)
    print(result.stdout)
else:
    print('Fehler: load zu hoch, HEPScore wird NICHT gestartet.')
