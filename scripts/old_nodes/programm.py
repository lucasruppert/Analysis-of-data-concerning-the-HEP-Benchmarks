import tools as t


def main():
    t.subprocess.run(["ipmi-sensors -r 35,36 --comma-separated-output --no-sensor-type-output --no-header-output"], shell = True)
    name = t.subprocess.run(['hostname'], shell=True, capture_output = True, text = True)
    name = name.stdout.split('.')[0]
    now = t.datetime.datetime.now().strftime('%d%m_%H%M')

    speed_names = []
    for i in range(40):
        speed_names.append(f'speed{i}_{name}')
    speed_names = ','.join(speed_names)

    f = open(f"file_{now}_{name}.csv", "w")
    f.write(f"time_{name},load_{name},PS1_{name},PS2_{name},{speed_names}")
    f.close()
    print(f"file_{now}_{name}.csv")
    
    while True:
        time = t.get_time()
        load = t.get_load()
        speed = t.get_speed()
        PS1, PS2 = t.get_power()
        f = open(f"file_{now}_{name}.csv", "a")
        f.write(f"\n{time},{load},{PS1},{PS2},{speed}")
        f.close()
        #print("#", end='')
        t.sleep(30)



if __name__ == "__main__":
    main()
