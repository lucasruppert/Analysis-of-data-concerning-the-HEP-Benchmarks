import json
from functions import get_ncores, get_hs_version
import subprocess
import pandas as pd
import numpy as np

def get_freq(run, node):
    '''reads the raw data file of the specified run on the node and returns the mean of all frequency measurements'''

    df = pd.read_csv(f'../../03_input_data/run_{run}/{node}/file_{run}_{node}.csv')
    if len(df.keys()) > 1000:
        raise TypeError('wrong pd.Dataframe format')

    freq = np.array([])

    nr_of_speed = 40
    if len(df.keys()) > 100:
        nr_of_speed = 256
    
    if 'speed0' in df.keys():
        for i in range(nr_of_speed):
            freq = np.append(freq, df[f'speed{i}'].to_numpy() / 1000)
    
    else:
        for i in range(nr_of_speed):
            freq = np.append(freq, df[f'speed{i}_{node}'].to_numpy() / 1000)
    
    return round(freq.mean(), -2), np.std(freq)
    


if __name__ == "__main__":
    nodes = ['n4505', 'n4506', 'n4507', 'n4508', 'n2119', 'n2120', 'n2121', 'n2122']


    runs = subprocess.run(['ls ../../03_input_data'], shell=True, text=True, capture_output=True)
    runs = runs.stdout.split()

    for node in nodes:
        f = open(f'../../03_input_data/local_catalog_{node}.csv', 'w')
        f.write('run,node,hs23,freq,d_freq,ncores,hs_version')
        f.close()


    i = 0
    for run in runs:
        present_nodes = subprocess.run([f'ls ../../03_input_data/{run}'], shell=True, text=True, capture_output=True)
        present_nodes = present_nodes.stdout.split()

        for node in present_nodes:
            if node in nodes:
                try:
                    with open(f'../../03_input_data/{run}/{node}/bmkrun_report.json', 'r') as report:
                        data = json.load(report)
                    
                    hs23 = data['profiles']['hepscore']['score']
                    ncores = get_ncores(run.split('run_')[1], node)
                    version = get_hs_version(run.split('run_')[1], node)
                    frequency, delta_frequency = get_freq(run.split('run_')[1], node)

                    

                    f = open(f'../../03_input_data/local_catalog_{node}.csv', 'a')
                    f.write(f'\n{run},{node},{hs23},{frequency},{delta_frequency},{ncores},{version}')
                    f.close()

                except:
                    print(run)
    
