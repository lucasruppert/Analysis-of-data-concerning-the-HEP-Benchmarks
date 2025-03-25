import functions as fct
import numpy as np
import pandas as pd
from datetime import timedelta, datetime


if __name__ == "__main__":
    nodes = ['n4505', 'n4506', 'n4507', 'n4508', 'n2119', 'n2120', 'n2121', 'n2122']
    catalog = fct.create_catalog(nodes)
    
    runs = np.unique(catalog['run'].to_numpy())

    for run in runs:
        nodes = catalog[catalog['run'] == run]['node'].to_numpy()
        stop, start, delta, time_in_sec = fct.get_max_runtime(run, nodes=nodes)

        for node in nodes:
            df = fct.create_df(run, node, stop, start, catalog)
            df.to_csv(f'../../04_output_data/new_nodes/data_{run}_{node}.csv', index=False)

