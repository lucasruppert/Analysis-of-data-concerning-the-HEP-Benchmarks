import subprocess
import datetime
from time import sleep


def get_load():
    '''fuehrt "uptime" aus und gibt den aktuellen system-load als float aus'''

    result = subprocess.run(["uptime"], shell = True, capture_output = True, text = True)
    if result.returncode == 0:
        load = float(result.stdout.split()[-3].removesuffix(',').replace(',', '.'))
        return load
    
    else:
        return None
    

def get_time():
    '''gibt die aktuelle Zeit als string aus'''

    time = datetime.datetime.now()
    
    return time.strftime('%d/%m/%y %H:%M:%S')


def get_power():
    '''fuehrt einen impi-befehl aus und formatiet das erhaltene ergebnis in zwei float-Werte mit Einheit Watt'''

    result = subprocess.run(["ipmi-sensors -r 35,36 --comma-separated-output --no-sensor-type-output --no-header-output"], shell = True, capture_output = True, text = True)
    if result.returncode == 0:
        PS1, PS2 = float(result.stdout.split(',')[2]), float(result.stdout.split(',')[-3])
        return PS1, PS2
    
    else:
        return None, None
    

def get_speed():
    '''fragt am Termial einen Befehl ab und gibt die atuelle Taktfrequenz als float zuruck'''

    result = subprocess.run(["cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq"], shell = True, capture_output = True, text = True)
    if result.returncode == 0:
        result = result.stdout.split()
        result = ','.join(result)
        return result
    
    else:
        return None
    

def get_runname():
    '''holt aus einer .txt Datei den zwischengespicherten Ordnernamen des aktuellen HEPScore-run (Speicherung im measurent.sh)'''

    result = subprocess.run(['cat /adm/lradmin/data/run_names.txt'], shell=True, capture_output = True, text = True)
    return result.stdout.split('\n')[0]


def get_hostname():
    '''ruft im Shell den hostname ab und gibt die Nummer des Knoten aus'''

    name = subprocess.run(['hostname'], shell=True, capture_output = True, text = True)
    name = name.stdout.split('.')[0]
    #name = name.split('0')[1]
    return name



if __name__ == "__main__":
    print(get_speed())
    print(get_time())
    print(get_load())
    print(get_power())
    print(get_hostname())
    print(get_runname())
