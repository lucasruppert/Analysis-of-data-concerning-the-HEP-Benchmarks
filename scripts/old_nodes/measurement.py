import tools as t


def main():
    name = t.get_hostname()

    now = t.get_runname()

    #creating the file and the columns headers
    speed_names = []
    for i in range(40):
        speed_names.append(f'speed{i}_{name}')
    speed_names = ','.join(speed_names)

    f = open(f"/adm/lradmin/data/run_{now}/file_{now}_{name}.csv", "w")
    f.write(f"time_{name},load_{name},PS1_{name},PS2_{name},{speed_names}")
    f.close()
    print(f"/adm/lradmin/data/run_{now}/file_{now}_{name}.csv")
    
    k = 0
    while True:
    #i = 0
    #while i < 1200:
    #    i += 1
        time = t.get_time()
        load = t.get_load()
        speed = t.get_speed()
        PS1, PS2 = t.get_power()
        f = open(f"/adm/lradmin/data/run_{now}/file_{now}_{name}.csv", "a")
        f.write(f"\n{time},{load},{PS1},{PS2},{speed}")
        f.close()
        #print("#", end='')
        t.sleep(30)

        if load < 3:
            k += 1
        else:
            k = 0
        
        if k > 30:
            break


if __name__ == "__main__":
    main()