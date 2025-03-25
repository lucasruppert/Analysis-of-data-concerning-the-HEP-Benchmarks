import functions as fct
import numpy as np
import pandas as pd
from datetime import timedelta, datetime


def create_superdf(filters: list[list[str, str | float]], nodes: list[str]) -> pd.DataFrame:
    catalog = fct.create_catalog(nodes)

    for filter in filters:
        catalog = catalog[catalog[filter[0]] == filter[1]]
    
    dfs = []
    for row in catalog.itertuples():
        dfs.append(pd.read_csv(f'../../04_output_data/new_nodes/data_{row[1]}_{row[2]}.csv'))

    return pd.concat(dfs)


if __name__ == "__main__":
    create_superdf(filters=[['hs_version', 'v1.5']],
                   nodes=['n4505', 'n4506', 'n4507', 'n4508']).to_csv('../../04_output_data/new_nodes/superdf_old_nodes.csv', index=False)
    
    create_superdf(filters=[['hs_version', 'v1.5']],
                   nodes=['n2119', 'n2120', 'n2121', 'n2122']).to_csv('../../04_output_data/new_nodes/superdf_new_nodes.csv', index=False)