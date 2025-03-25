import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
from datetime import datetime, timedelta
from scipy import integrate, optimize
import yaml
import json


## two small helpfull functions 

def seconds_to_hours(sec: float) -> float:
    '''converts the given seconds to hours'''
    return (sec/60)/60


def read_df(path: str):
    '''reads pd.Dataframe from .csv and converts the time ('%Y-%m-%d %H:%M:%S') to a datetime object'''
    
    df = pd.read_csv(path)
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')

    return df



## The following functions (most with get_) are used to extract certain values from log-files of different measurements
## Some of the retrieved values are used for filtering the data (like hs_version) while others are needed for the analysis (like hs_value)

def run_duration(run: str, node: str, out: bool = True) -> float:
    """
    Retrieves the duration of the specified run on the given node from 
    the `hep-benchmark-suite.log` file.

    Parameters
    ----------
    run : str
        The identifier of the run.
    node : str
        The name of the node.
    out : bool, optional
        If True, additional output may be provided. Default is True.

    Returns
    -------
    float
        The duration of the run in seconds.
    """


    result = subprocess.run([f'cat ../../03_input_data/run_{run}/{node}/hep-benchmark-suite.log'], shell=True, capture_output=True, text=True)
    
    result = result.stdout.split()
    start = f'{result[0]} {result[1]}'
    stop = f'{result[-9]} {result[-8]}'
    
    start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S,')
    stop = datetime.strptime(stop, '%Y-%m-%d %H:%M:%S,')
    diff = stop - start
    diff = diff.total_seconds()

    if out:
        return start, stop

    return diff


def get_max_runtime(run: str, nodes: list[str]) -> tuple:
    """
    Retrieves data concerning the maximum runtime for a given run among its nodes.

    Parameters
    ----------
    run : str
        The identifier of the run.
    nodes : list of str
        A list of nodes involved in the run.

    Returns
    -------
    tuple
        A tuple containing:
        - min_start_time : datetime
            The earliest start time among all nodes.
        - max_stop_time : datetime
            The latest stop time among all nodes.
        - runtime_diff : timedelta
            The difference between the start and stop times.
        - runtime_array : np.ndarray
            A NumPy array representing the runtime with 1-second steps.
    """


    stops = []
    starts = []

    for node in nodes:
        start, stop = run_duration(run, node, out=True)
        stop = (stop + timedelta(seconds=30))
        start = (start - timedelta(seconds=30))
        
        stops.append(stop)
        starts.append(start)

    stop = max(stops)
    start = min(starts)
    delta = (stop - start).total_seconds()
    time_in_sec = np.arange(0, delta, 1)

    return stop, start, delta, time_in_sec


def get_hepscore(run: str, node: str) -> float:
    """
    Retrieves the HEPScore of the specified run on the given node from 
    the `bmkrun_report.json` file.

    Parameters
    ----------
    run : str
        The identifier of the run.
    node : str
        The name of the node.

    Returns
    -------
    float
        The HEPScore value for the specified run and node.
    """


    with open(f'../../03_input_data/run_{run}/{node}/bmkrun_report.json', 'r') as report:
        data = json.load(report)

    hepscore = data['profiles']['hepscore']['score']

    return hepscore


#    '''gets the power configuration of the specified run on the node from the bmkrun_report.json file '''
def get_power_policy(run: str, node: str) -> float:
    """
    Retrieves the power configuration of the specified run on the given node 
    from the `bmkrun_report.json` file.

    Parameters
    ----------
    run : str
        The identifier of the run.
    node : str
        The name of the node.

    Returns
    -------
    float
        The power configuration value for the specified run and node.
    """

    with open(f'../../03_input_data/run_{run}/{node}/bmkrun_report.json', 'r') as report:
        data = json.load(report)

    power_policy = data['host']['HW']['CPU']['Power_Policy']

    return power_policy



def get_freq(run: str, node: str) -> float:
    """
    Reads the raw data file of the specified run on the given node and 
    returns the mean of all frequency measurements.

    Parameters
    ----------
    run : str
        The identifier of the run.
    node : str
        The name of the node.

    Returns
    -------
    float
        The mean frequency measured during the run.
    """


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
    
    return round(freq.mean(), -2)


def get_ncores(run: str, node: str) -> int:
    """
    Retrieves the number of virtual cores (vcores) used by HEPScore23 
    for the specified run on the given node.

    Parameters
    ----------
    run : str
        The identifier of the run.
    node : str
        The name of the node.

    Returns
    -------
    int
        The number of virtual cores used for the run.
    """


    with open(f'../../03_input_data/run_{run}/{node}/run_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    if config['hepscore']['config'] == 'default':
        cores = config['global']['ncores']
    else:
        cores = config['global']['tags']['ncores']
    
    return cores


def get_hs_version(run: str, node: str) -> str:
    """
    Retrieves the version of HEPScore23 used for the specified run on the given node 
    from the `run_config.yaml` file.

    Parameters
    ----------
    run : str
        The identifier of the run.
    node : str
        The name of the node.

    Returns
    -------
    str
        The HEPScore23 version used for the run.
    """


    with open(f'../../03_input_data/run_{run}/{node}/run_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    version = config['hepscore']['version']

    return version



## The following functions are used in other python scripts to catalog the original data and create the pd.Dataframes used for analysis

def cut_to_runtime(run: str, node: str, path: str) -> pd.DataFrame:
    """
    Filters the measurement data to include only the points recorded during 
    the execution of the HEPScore23 run.

    Parameters
    ----------
    run : str
        The identifier of the run.
    node : str
        The name of the node.
    path : str
        The file path to the measurement data.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing only the measurement data recorded during 
        the execution of the HEPScore23 run.

    Notes
    -----
    The helper function read_df is used to convert the time into a datetime object.
    When working with a different format this needs to be done differently (here).
    """

    df = read_df(path)
    

    start, stop = run_duration(run, node, out=True)
    df = df[df['time'] < (stop + timedelta(seconds=30))]
    df = df[df['time'] > (start - timedelta(seconds=30))]

    return df



def create_df(run: str, node: str, stop: datetime, start: datetime, catalog) -> pd.DataFrame:
    """
    Reads the raw measurement data of the specified run on the given node and 
    returns a DataFrame suitable for data analysis.

    Parameters
    ----------
    run : str
        The identifier of the run.
    node : str
        The name of the node.
    stop : datetime
        The stop time of the HEPScore run.
    start : datetime
        The start time of the HEPScore run.
    catalog : 
        The data source or catalog containing the measurement data.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the processed measurement data, ready for analysis.

    Notes
    -----
    The start and stop times can be obtained using `functions.get_maxruntime(run, nodes)`.
    """


    df = pd.read_csv(f'../../03_input_data/run_{run}/{node}/file_{run}_{node}.csv')

    df['node'] = node
    df['run'] = run

    ### following exceptions because of some inconsitencies in the format of the first measurements
    try:
        df['time'] = pd.to_datetime(df['time'], format='%d/%m/%y %H:%M:%S')
        df['PS'] = df[f'PS1'] + df[f'PS2']
        df.drop(columns=['PS1', 'PS2'], inplace=True)
    except KeyError:
        try:
            df[f'time_{node}'] = pd.to_datetime(df[f'time_{node}'], format='%d/%m/%y %H:%M:%S')
            df['PS'] = df[f'PS1_{node}'] + df[f'PS2_{node}']
            df.drop(columns=[f'PS1_{node}', f'PS2_{node}'], inplace=True)
            df.rename(columns={f'load_{node}' : 'load', f'time_{node}': 'time'}, inplace=True)
        except:
            print(run, node)
    except ValueError:
        df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
        df['PS'] = df[f'PS1'] + df[f'PS2']
        df.drop(columns=['PS1', 'PS2'], inplace=True)
    

    df = df[df['time'] < (stop + timedelta(seconds=30))]
    df = df[df['time'] > (start - timedelta(seconds=30))]
    
    df['hs23'] = get_hepscore(run, node)        
    df['runtime [h]'] = seconds_to_hours(run_duration(run, node, out=False))
    df['ncores'] = get_ncores(run, node)

    ### too long and unelegant fix of switching format
    freq = np.array([])
    columns = []
    nr_of_speed = 40
    if len(df.keys()) > 100:
        nr_of_speed = 256
    
    if 'speed0' in df.keys():
        for i in range(nr_of_speed):
            freq = np.append(freq, df[f'speed{i}'].to_numpy() / 1000)
            columns.append(f'speed{i}')
    
    else:
        for i in range(nr_of_speed):
            freq = np.append(freq, df[f'speed{i}_{node}'].to_numpy() / 1000)
            columns.append(f'speed{i}_{node}')

    df['freq'] = round(freq.mean(), -2)
    df['delta_freq'] = np.std(freq)
    df.drop(columns=columns, inplace=True)
    #df['freq'] = catalog[(catalog['run'] == run) & (catalog['node'] == node)]['freq'].to_list()[0]
    df['power_policy'] = get_power_policy(run, node)

    #df['time [s]'] = df.apply(lambda row: (row['time'] - df['time'][0]).total_seconds() + (df['time'][0] - start).total_seconds(), axis=1)
    #df['time [h]'] = df.apply(lambda row: seconds_to_hours((row['time'] - df['time'][0]).total_seconds() + (df['time'][0] - start).total_seconds()), axis=1)
    df['time [s]'] = df.apply(lambda row: (row['time'] - start).total_seconds(), axis=1)
    df['time [h]'] = df.apply(lambda row: seconds_to_hours((row['time'] - start).total_seconds()), axis=1)


    return df


def create_catalog(nodes: list[str]) -> pd.DataFrame:
    '''takes the file local_catalog_{node}.csv '''

    catalogs = []
    for node in nodes:
        catalog = pd.read_csv(f'../../03_input_data/local_catalog_{node}.csv')
        try:
            catalog['run'] = catalog.apply(lambda row: row['run'].split('run_')[1], axis=1).to_numpy()
        except:
            pass
        catalogs.append(catalog)

    catalog = pd.concat(catalogs)

    return catalog




## The following functions are used to extraxt the wanted data from all measurements (contained in a "superdf")


def power_percentile_mean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a column to the given DataFrame containing the mean of the percentiles 
    0.7 to 0.9 of the power-column `PS`.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame containing a column named `PS` for power values.

    Returns
    -------
    pd.DataFrame
        The input DataFrame with an additional column containing the mean of 
        the percentiles 0.7 to 0.9 of the `PS` column.
    """


    dfs = []
    runs = list(set(df['run']))
    nodes = list(set(df['node']))

    for run in runs:
        for node in nodes:
            temp_df = df[(df['run'] == run) & (df['node'] == node)]
            percentiles = []

            for percentile in np.linspace(0.7, 0.9, 10):
                percentiles.append(temp_df['PS'].quantile(q=percentile))
            
            pm = np.mean(percentiles)


            temp_df = temp_df.assign(ppm=pm)
            dfs.append(temp_df)
    
    return pd.concat(dfs)


def data_to_numpy(df: pd.DataFrame, mode: str, ppm: bool = True, per_vcore: bool = True):
    """
    Converts the given DataFrame into NumPy arrays for plotting in the specified configuration.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame containing the necessary data.
    mode : str
        Specifies if the DataFrame is grouped by `ncores` or `frequency` (`ncores` | `freq`).
    ppm : bool, optional
        If True, returns the power percentile mean (created by `power_percentile_mean`) 
        instead of the power mean. Default is True.
    per_vcore : bool, optional
        If True, divides the returned power and `hs` arrays by the number of vcores. 
        Default is True.

    Returns
    -------
    tuple
        A tuple containing the following NumPy arrays:
        - ref : ndarray
            Frequency or ncores as specified.
        - power : ndarray
            The power values.
        - power_err : ndarray
            The error in power values.
        - hs : ndarray
            The harmonic sum.
        - hs_err : ndarray
            The error in harmonic sum.
        - runtime : ndarray
            The runtime values.
        - runtime_err : ndarray
            The error in runtime values.
    """

    df = power_percentile_mean(df)
    ref = df.groupby(mode)[mode].mean().to_numpy()

    runtime = df.groupby(mode)['runtime [h]'].mean().to_numpy()
    runtime_err = df.groupby(mode)['runtime [h]'].std().to_numpy()

    if per_vcore:
        hs = (df.groupby([mode, 'node'])['hs23'].mean() / df.groupby([mode, 'node'])['ncores'].mean()).groupby(mode).mean().to_numpy()
        hs_err = (df.groupby([mode, 'node'])['hs23'].mean() / df.groupby([mode, 'node'])['ncores'].mean()).groupby(mode).std().to_numpy()
        if ppm:
            power = ((df.groupby([mode, 'node'])['ppm'].mean() / 4) / df.groupby([mode, 'node'])['ncores'].mean()).groupby(mode).mean().to_numpy()
            power_err = ((df.groupby([mode, 'node'])['ppm'].mean() / 4) / df.groupby([mode, 'node'])['ncores'].mean()).groupby(mode).std().to_numpy()
        else:
            power = ((df.groupby([mode, 'node'])['PS'].mean() / 4) / df.groupby([mode, 'node'])['ncores'].mean()).groupby(mode).mean().to_numpy()
            power_err = ((df.groupby([mode, 'node'])['PS'].mean() / 4) / df.groupby([mode, 'node'])['ncores'].mean()).groupby(mode).std().to_numpy()
    
    else:
        hs = df.groupby([mode, 'node'])['hs23'].mean().groupby(mode).mean().to_numpy()
        hs_err = df.groupby([mode, 'node'])['hs23'].mean().groupby(mode).std().to_numpy()
        if ppm:
            power = (df.groupby([mode, 'node'])['ppm'].mean() / 4).groupby(mode).mean().to_numpy()
            power_err = (df.groupby([mode, 'node'])['ppm'].mean() / 4).groupby(mode).std().to_numpy()
        else:
            power = (df.groupby([mode, 'node'])['PS'].mean() / 4).groupby(mode).mean().to_numpy()
            power_err = (df.groupby([mode, 'node'])['PS'].mean() / 4).groupby(mode).std().to_numpy()
    
    return ref, power, power_err, hs, hs_err, runtime, runtime_err

