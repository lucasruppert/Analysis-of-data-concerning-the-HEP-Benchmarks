import tools as t


def main():
    name = t.get_hostname()
    now = t.get_runname()

    #creating the file and the columns headers
    speed_names = []
    for i in range(40):
        speed_names.append(f'speed{i}')
    speed_names = ','.join(speed_names)

    f = open(f"/adm/lradmin/data/run_{now}/file_{now}_{name}.csv", "w")
    f.write(f"time,load,PS1,PS2,{speed_names}")
    f.close()
    print(f"/adm/lradmin/data/run_{now}/file_{now}_{name}.csv")
    
    
    i = 1
    while True:
        time = t.get_time()
        load = t.get_load()
        speed = t.get_speed()
        PS1, PS2 = t.get_power()
        f = open(f"/adm/lradmin/data/run_{now}/file_{now}_{name}.csv", "a")
        f.write(f"\n{time},{load},{PS1},{PS2},{speed}")
        f.close()

        with open('/adm/lradmin/data/start_stop.txt') as f:
            start_stop = f.read()

        start_stop = start_stop.split()[0]

        if start_stop == 'stop':
            break

        t.sleep(30)

        
            
        


if __name__ == "__main__":
    main()