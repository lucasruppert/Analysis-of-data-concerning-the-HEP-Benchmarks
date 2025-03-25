import subprocess
import pandas as pd

if __name__ == "__main__":

    nodes = ['n2119', 'n2120', 'n2121', 'n2122'] #['n4505', 'n4506', 'n4507', 'n4508', 
        
    for node in nodes:
        subprocess.run([f'scp lradmin@{node}.bfg.uni-freiburg.de:/adm/lradmin/data/hepscores_{node}.csv ../../03_input_data/.'],
                        text=True, shell=True, capture_output=True)
        subprocess.run([f'mv ../../03_input_data/hepscores_{node}.csv ../../03_input_data/server_catalog_{node}.csv'],
                        text=True, shell=True, capture_output=True)

        server_catalog = pd.read_csv(f'../../03_input_data/server_catalog_{node}.csv')
        local_catalog = pd.read_csv(f'../../03_input_data/local_catalog_{node}.csv')

        new_local_catalog = pd.read_csv(f'../../03_input_data/local_catalog_{node}.csv')
        save = True

        server_catalog_runs = server_catalog['run'].to_numpy()
        local_catalog_runs = local_catalog['run'].to_numpy()

        for run in server_catalog_runs:
            if run not in local_catalog_runs:
                try:
                    subprocess.run([f'mkdir ../../03_input_data/{run}'], shell=True, text=True, capture_output=True)
                    subprocess.run([f'mkdir ../../03_input_data/{run}/{node}'], shell=True, text=True, capture_output=True)
                except:
                    pass

                try:
                    subprocess.run([f'scp lradmin@{node}.bfg.uni-freiburg.de:/adm/lradmin/data/{run}/* ../../03_input_data/{run}/{node}/'], 
                                shell=True, text=True, capture_output=True)
                except:
                    print(run, node)
                    save = False

                new_local_catalog = pd.concat([new_local_catalog, server_catalog[server_catalog['run'] == run]])
            

        if save:
            new_local_catalog.to_csv(f'../../03_input_data/local_catalog_{node}.csv')
        print(f'done {node}')