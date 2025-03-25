from functions import read_df, get_ncores

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import subprocess
from datetime import datetime, timedelta
from scipy import integrate, optimize

## The purpose of this script is to define lengthy functions which are used multiple times during the analysis to plot specific data


def benchmarks():
    """helper function to quickly obtain a list of the individual HEP-workloads used by the HEPScore23-benchmark (Dez 2024)"""

    bmks = ['atlas-gen_sherpa-ma-bmk', 'atlas-reco_mt-ma-bmk', 'cms-gen-sim-run3-ma-bmk', 'cms-reco-run3-ma-bmk', 'lhcb-sim-run3-ma-bmk', 'belle2-gen-sim-reco-ma-bmk',
                'alice-digi-reco-core-run3-ma-bmk']

    return bmks


def get_runtimes_individual_bmks_ncores(run: str, node: str) -> tuple:
    """
    Retrieves the start and stop timestamps of the individual benchmarks 
    of the HEPScore23 benchmark.

    Parameters
    ----------
    run : str
        The identifier of the run.
    node : str
        The name of the node.

    Returns
    -------
    tuple
        A tuple containing:
        - start_times : list of datetime
            A list of start timestamps for the individual benchmarks.
        - stop_times : list of datetime
            A list of stop timestamps for the individual benchmarks.
    """


    with open(f'../../03_input_data/run_{run}/{node}/hep-benchmark-suite.log', 'r') as f:
        log = f.read()

    log = log.split()
    bmks = ['atlas-gen_sherpa-ma-bmk', 'atlas-reco_mt-ma-bmk', 'cms-gen-sim-run3-ma-bmk', 'cms-reco-run3-ma-bmk', 'lhcb-sim-run3-ma-bmk', 'belle2-gen-sim-reco-ma-bmk',
            'alice-digi-reco-core-run3-ma-bmk']
    times = {}

    for i in range(len(log)):
        for bmk in bmks:
            if bmk == log[i]:
                times[bmk] = datetime.strptime(" ".join([log[i-8], log[i-7].removesuffix(',')]), '%Y-%m-%d %H:%M:%S')

        if 'hepscore.hepscore:gen_score' == log[i]:
            times['ende'] = datetime.strptime(" ".join([log[i-2], log[i-1].removesuffix(',')]), '%Y-%m-%d %H:%M:%S')

    return times


def make_individual_bmk_data_ncores(run: str, node: str):
    """
    Processes benchmark data for individual benchmarks, extracting and organizing 
    the time, power, and load data for each benchmark in the run.

    Parameters
    ----------
    run : str
        The identifier of the run.
    node : str
        The name of the node.

    Returns
    -------
    tuple
        A tuple containing:
        - time : dict
            A dictionary where the keys are benchmark names and the values are the corresponding time data.
        - load : dict
            A dictionary where the keys are benchmark names and the values are the corresponding load data.
        - power : dict
            A dictionary where the keys are benchmark names and the values are the corresponding power data.
        - freq : float
            The frequency value associated with the benchmark data.
    """


    df_temp = read_df(f'../../04_output_data/data_{run}_{node}.csv')

    times = get_runtimes_individual_bmks_ncores(run, node)


    bmks = ['atlas-gen_sherpa-ma-bmk', 'atlas-reco_mt-ma-bmk', 'cms-gen-sim-run3-ma-bmk', 'cms-reco-run3-ma-bmk', 'lhcb-sim-run3-ma-bmk', 'belle2-gen-sim-reco-ma-bmk',
            'alice-digi-reco-core-run3-ma-bmk']
    power, load, time = {}, {}, {}

    for i in range(len(bmks) - 1):
        df_loop = df_temp[df_temp['time'] <= times[bmks[i + 1]]]
        df_loop = df_loop[df_loop['time'] >= times[bmks[i]]]

        power[bmks[i]] = df_loop['PS'].to_numpy()
        load[bmks[i]] = df_loop['load'].to_numpy()
        time[bmks[i]] = df_loop['time [h]'].to_numpy()

    i = -1

    df_loop = df_temp[df_temp['time'] <= times['ende']]
    df_loop = df_loop[df_loop['time'] >= times[bmks[i]]]

    power[bmks[i]] = df_loop['PS'].to_numpy()
    load[bmks[i]] = df_loop['load'].to_numpy()
    time[bmks[i]] = df_loop['time [h]'].to_numpy()

    freq = df_temp['freq'][5]

    return time, load, power, freq



def plot_lifeline_separate(run: str, node: str, savefig=None, ncol=2, fontsize=9):
    """
    Plots the time vs load and time vs power for a benchmark run as separate figures. 
    The individual benchmarks are color-coded. If `savefig` is specified, the function saves:
    - The time vs power plot
    - The time vs load plot
    - A common legend, plotted and saved as a separate figure.

    Parameters
    ----------
    run : str
        The identifier of the run.
    node : str
        The name of the node.
    savefig : list of str or None, optional
        A list containing the file paths to save the figures. The first item in the list is used for saving the 
        time vs power plot, the second for saving the time vs load plot, and the third for saving the common legend.
        If None, the figures are shown instead of saved.
    ncol : int, optional
        The number of columns in the legend. Default is 2.
    fontsize : int, optional
        The font size of the legend. Default is 9.

    Returns
    -------
    None
        This function plots two figures: one for time vs power and one for time vs load. 
        It also optionally saves the figures and the common legend to the specified file paths.
    """


    time, load, power, freq = make_individual_bmk_data_ncores(run, node)
    ncores = get_ncores(run, node)

    bmks = ['atlas-gen_sherpa-ma-bmk', 'atlas-reco_mt-ma-bmk', 'cms-gen-sim-run3-ma-bmk', 'cms-reco-run3-ma-bmk', 'lhcb-sim-run3-ma-bmk', 'belle2-gen-sim-reco-ma-bmk',
                'alice-digi-reco-core-run3-ma-bmk']

    ##plots time vs power
    plt.gcf().clear()
    fig, ax = plt.subplots()
    legend_elements = []
    
    for bmk in bmks:
        ax.plot(time[bmk], power[bmk], linewidth=1)#, color=colors[bmk]
        ax.fill_between(y1=power[bmk], x=time[bmk])#, color=colors[bmk]

        last_line = ax.lines[-1]  # Das letzte Line2D-Objekt im aktuellen Axes
        last_color = last_line.get_color()
        label = bmk.split('-ma-')[0].split('-run3')[0]
        legend_elements.append(Line2D([0], [0], marker='s', color='w', label=label, 
                                      markerfacecolor=last_color, markersize=10))

   

    color = 'tab:red'
    ax.set_ylabel('power [W]', color=color)
    ax.set_xlabel('time [h]')
    ax.tick_params(axis='y', labelcolor=color)
    ax.grid(axis='y')

    fig.set_figwidth(10)
    fig.set_figheight(5)
    

    if savefig == None:
        plt.show()
    else:
        plt.savefig(savefig[0], dpi=500)
    
    ## plots legend
    legend_fig = plt.figure()
    legend_fig.legend(handles=legend_elements, ncol=ncol, fontsize=fontsize, loc='center')

    if savefig == None:
        plt.show()
    else:
        plt.savefig(savefig[2], dpi=100)




    ## plots time vs load
    plt.gcf().clear()
    fig, ax = plt.subplots()
    legend_elements = []

    for bmk in bmks:
        ax.plot(time[bmk], load[bmk], linewidth=1)
        ax.fill_between(y1=load[bmk], x=time[bmk])

        last_line = ax.lines[-1]
        last_color = last_line.get_color()
        label = bmk.split('-ma-')[0].split('-run3')[0]
        legend_elements.append(Line2D([0], [0], marker='s', color='w', label=label, 
                                      markerfacecolor=last_color, markersize=10))


    color = 'tab:blue'
    ax.axhline(ncores, color='k')
    ax.set_ylabel('load', color=color)
    ax.set_xlabel('time [h]')
    ax.tick_params(axis='y', labelcolor=color)
    ax.grid(axis='y')
 
    fig.set_figwidth(10)
    fig.set_figheight(5)

    if savefig == None:
        plt.show()
    else:
        plt.savefig(savefig[1], dpi=500)




def plot_power_hist(filter: list, df, savefig=None, binwidth: float = 6.25):
    """
    Plots a histogram of all measured PS-values for a given filter, 
    the truncated mean, and the mean. The filter can be set to a frequency, 
    number of vCores, node, run, etc.

    Parameters
    ----------
    filter : list
        A list specifying the filter criteria (e.g., frequency, vCores, node, run).
    df : pd.DataFrame
        The DataFrame containing the measured PS-values.
    savefig : str or None, optional
        The file path to save the figure, if specified. Default is None, which does not save the figure.
    binwidth : float, optional
        The width of the histogram bins. Default is 6.25.
    
    Returns
    -------
    None
        This function plots a histogram and optionally saves it to a file.
    """


    temp_df = df[df[filter[0]] == filter[1]]

    temp_df['PS'] = temp_df['PS'].to_numpy() / 4
    temp_df['ppm'] = temp_df['ppm'].to_numpy() / 4

    fig, ax = plt.subplots()

    temp_df['PS'].hist(bins=np.arange(100, max(temp_df['PS']), binwidth), ax=ax)
    ax.axvline(temp_df['PS'].mean(), color='k', label='mean')
    ax.axvline(np.mean(temp_df.groupby(['run', 'node'])['ppm'].mean().to_numpy()), color='red', label='truncated mean')


    ax.set_xlabel('power [W]')

    ax.legend(loc=(.01,.7), fontsize=13)

    #fig.tight_layout()
    fig.set_figheight(4)
    fig.set_figwidth(5)

    if savefig == None:
        plt.show()
    else:
        plt.savefig(savefig, dpi=100)
