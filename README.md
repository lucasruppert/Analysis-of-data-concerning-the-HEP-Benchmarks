<<<<<<< HEAD
# Analysis-of-data-concerning-the-HEP-Benchmarks
This is the Code I wrote during my Bachelors Thesis at the Schumacher Group at Uni Freiburg
=======
## Analysis of the HEPScore23-benchmark and its power consumption on the ATLAS-BFG cluster

## Folder structure
The projects code requires the following folder structure:

```
├── 02_code
│   ├── notebooks
│   ├── python
│   └── scripts
├── 03_input_data
│   ├── run_%d%m_%H%M
│   ├── run_%d%m_%H%M
.   ...
.   
├── 04_output_data
│   ├── co2_production.json
│   └── energy-charts_Public_net_electricity_generation_in_Germany_in_2023.csv
└── 05_plots
```

**02_code**<br>
This folder contains all the code:<br>
- *notebooks* contains jupyter notebooks mostly used for plotting the results
- *python* contains python scripts who either handle the raw data from **03_input_data** to produce the analyzable data of **04_output_data** or provide vital functions used in the notebooks
- *scripts* contains the measurement process meant to be executed only on servers (requires ipmi support)
<br><br>

**03_input_data**<br>
This folder contains the raw measurement data of the individual benchmark runs in the following folder structure:
```
run_%d%m_%H%M
.   ├── n4505
.   │   ├── bmkrun_report.json
.   │   ├── file_%d%m_%H%M_n4505.csv
    │   ├── hep-benchmark-suite.log
    │   └── run_config.yaml
    ├── n4506
    .
    .
    .
```

The naming convention *%d%m_%H%M* (python datetime convention) produces for a benchmark started at 15:13 on January 16th *1601_1513*.
<br><br>

**04_output_data**<br>
This folder will primarily contain output data created by python scripts from *02_code/python*.<br>
The two prerequisite files are needed for the analysis of $CO_2$-emissions. 
- co2_production.json contains data about the $CO_2$-emissions produced per kWh of different electricity sources ([IPCC](https://abdn.elsevierpure.com/en/publications/annex-iii-technology-specific-cost-and-performance-parameters)).
- energy-charts_Public_net_electricity_generation_in_Germany_in_2023.csv needs the **complete** data of the calender year 2023 from [Fraunhofer ISE energy charts](https://www.energy-charts.info/charts/power/chart.htm?l=en&c=DE&year=2023&source=public&legendItems=3x2vvv6&interval=year).


## Data handling and analysis

This is done with scripts from *02_code/notebooks*.<br>
- **functions.py** contains function used for all kinds of purposes, ranging from obtaining data from raw files to analysing the output data. It is mostly imported with `import functions as fct`.
- **plotting_functions.py** contains functions that plot and save data frequently needed for different parts of the analysis. It is imported with `import plotting_functions as pltfct`.<br><br>

The file **update_data.py** updates the data in 03_input_data automatically. To do this it needs a local catalog of the data produced by **catalog.py** However, it is highly customized with certain node- and usernames and should be approached concious of that.<br>
The scripts listed in the following should be executed in that order when working with raw data. Doing so should allow the notebooks to work without interruption.

1. **catalog.py** creates a catalog (csv-file) with information about the locally stored data in 03_input_data.
2. **create_output_data.py** removes unnecassary information from the raw data in 03_input_data and fixes some backwards compatibility issues in the column naming scheme. The complete pd.DataFrames are saved in 04_output_data.
3. **create_dfs.py** filters the pd.DataFrames in 04_output_data and creates a complete pd.DataFrame (saved in 04_output_data) of all data of a specified (in the `if __name__ == "__main__"` part) set of nodes. These DataFrames are the ones primarily used in the notebooks.
<br><br>

Most of the data analysis concering the HEPScore23-value and the power consumption is handled by the function `fct.data_to_numpy`.
<br>
In the thesis a truncated mean was used as a metric. Upon reviewing it shortly before handing it in I realized that the median is a simpler method offering similar compatibility to the data. Unfortunately, because of the time frame changes to the code and final draft of the thesis were not possible.


## Notebooks
- **old_nodes.ipynb** plots  and saves the wanted data concerning the older Intel nodes of the ATLAS-BFG cluster in .tex and .png format.
- **new_nodes.ipynb** plots  and saves the wanted data concerning the newer AMD nodes of the ATLAS-BFG cluster in .tex and .png format.
- **energy_supply_analysis.ipynb** analyzes, plots and saves data concerning the calculation of the ATLAS-BFG clusters $CO_2$-footprint.


## Measurements
The scripts which measures the data on the two different node types are contained in the folders *old_nodes* and *new_nodes*.<br>
The processes are the same in principle: **measurement_ncores_singlerun.sh** manages the data collection and storage while **start_hepscore_ncores_singlerun.sh** starts the benchmark in a wanted configuration and saves the output afterwards alongside the other data. The wanted configuration is passed on when deploying the latter cronjob as arguments. The script **init_ncores_config.sh** sets up the the hep-benchmark-suite in way for the measurement process to work.<br>
The scripts contain some absolute filepaths suited for my usernames during the thesis. I did not try to generalize it because of the reasons mentioned below.
<br><br>

While this process works it uses "communication" between the two processes via written keywords to txt-files (start_stop.txt). This is unelegant at the least and since it needs correctly timed sleep-commands also an errorrisk. I initially planned to write and document a process to schedule and configure the measurements easily. However, upon reviewing the hep-benchmark-suite gitlab documentation I realized that the measurement process is already implemented via the plugin CommandExecute.
<br>

The most convinient way would be to generalize the current versions of **init_ncores_config.sh** and **start_hepscore_ncores_singlerun.sh**.
This is attempted in the folder *02_code/measurements_v2*. The bash-script **suite_setup.sh** clones the git repositry of the [hep-benchmeark-suite](https://gitlab.cern.ch/hep-benchmarks/hep-benchmark-suite.git) into the $XDG_CONFIG_HOME directory and makes some adjustments to ensure that the **start_hep_bmk.sh** script can run properly. The python script **commandexec.py** distributes the settings in **commandexec.yml** for the benchark-suites CommandExecute plugin to the configuration files created by **suite_setup.sh**. This is responsible for the measurement process. The script **compatibility.py** converts the data from the json files to a csv-format to ensure that the whole analyzation described before is still possible if necessary.
<br><br>


## Words at the end
I hope this documentation and improvement upon the measurement process (by reading the **whole** GitLab documentation of the hep-benchmark-suite and implementing it rudementary) someday helps someone somehow. However, I realize that this code was written for a bachelors thesis and is probably a bit too basic and usecase specific, so please be careful when reusing (parts of) it.
>>>>>>> master
