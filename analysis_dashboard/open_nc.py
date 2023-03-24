'''
SHJewell, March 2, 2023

Utility for opening NetCDF4 geospatial data files
Based on a similar utility for my basic_geo_dashboard
This version has been altered to open time-independent post-analysis files.

These files have have (at least for now) the same basic core variables: temperature min, max and mean plus precipitation
The twist is that every one of these is the analysis of five years (or more) of data, including the min, max mean, median
and standard deviation. Each of these has a hyphenated variable name ie tasmaxAdjust-mean for the mean of the maximum
temperature
'''

import numpy as np
import pandas as pd
import netCDF4
from netCDF4 import Dataset
from dataclasses import dataclass
import dateutil.parser as dparser
import datetime
from operator import itemgetter


@dataclass
class multiVarNCSet:
    path: str
    vars: dict()
    def __post_init__(self):

        data_grp = Dataset(self.path, 'r')
        self.lats = data_grp.variables['lat'][:]
        self.lons = data_grp.variables['lon'][:]
        self.data = dict()
        self.analyses = ['min', 'max', 'mean', 'median', 'std']

        for _, var_name in list(self.vars.items()):

            for post in self.analyses:

                temp = np.ma.array(data_grp.variables[f'{var_name}_{post}'][:].filled(fill_value=np.nan), dtype=np.float16)
                self.data[f'{var_name}_{post}'] = temp

        data_grp.close()

    def ret_set(self, dset, analysis):

        return pd.DataFrame(self.data[f'{dset}_{analysis}'], index=self.lats, columns=self.lons)

    def ret_default_heuristic(self):

        diff = self.data[f'tasmaxAdjust_mean'] - self.data[f'tasminAdjust_mean']

        return diff / np.nanmax(diff)