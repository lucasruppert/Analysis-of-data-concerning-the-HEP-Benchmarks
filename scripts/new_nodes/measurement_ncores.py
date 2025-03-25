import tools as t


def main():
    name = t.get_hostname()
    now = t.get_runname()

    #creating the file and the columns headers
    speed_names = []
    for i in range(256):
        speed_names.append(f'speed{i}')
    speed_names = ','.join(speed_names)

    ### this part is only temporary to take a look at a specific property during measurement
    #dic = {}
    #for apendix in ['min', 'max', 'config']:
    #    dic[apendix] = []
    #    for i in range(256):
    #        dic[apendix].append(f'freq{i}_{apendix}')
    #    dic[apendix] = ','.join(dic[apendix])
    ###

    f = open(f"/adm/lradmin/data/run_{now}/file_{now}_{name}.csv", "w")
    f.write(f"time,load,PS1,PS2,{speed_names}")             #,{dic['min']},{dic['max']},{dic['config']}
    f.close()
    print(f"/adm/lradmin/data/run_{now}/file_{now}_{name}.csv")
    
    
    i = 1
    while True:
        time = t.get_time()
        load = t.get_load()
        speed = t.get_speed()
        PS1, PS2 = t.get_power()

        ### also only temporary
        #freq_min = t.get_speed(config='min')
        #freq_max = t.get_speed(config='max')
        #freq_config = t.get_speed_config()
        ###
        
        f = open(f"/adm/lradmin/data/run_{now}/file_{now}_{name}.csv", "a")
        f.write(f"\n{time},{load},{PS1},{PS2},{speed}")         #,{freq_min},{freq_max},{freq_config}
        f.close()

        with open('/adm/lradmin/data/start_stop.txt') as f:
            start_stop = f.read()

        start_stop = start_stop.split()[0]

        if start_stop == 'stop':
            break

        t.sleep(30)

        
            
        


if __name__ == "__main__":
    main()