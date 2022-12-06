import numpy as np

from netCDF4 import Dataset
from dataclasses import dataclass
import pickle
import sys
import tracemalloc

@dataclass
class NCSet:
    path: str
    var_name: str
    # lats: np.ma.core.MaskedArray
    # lons: np.ma.core.MaskedArray
    # time: np.ma.core.MaskedArray
    # # data: np.ma.core.MaskedArray  to be used to build an external database
    # min: np.ma.core.MaskedArray
    # max: np.ma.core.MaskedArray
    # median: np.ma.core.MaskedArray
    # var: np.ma.core.MaskedArray
    # # stddev: np.ma.core.MaskedArray


    '''
    I guess data classes don't need this if you have the hints above
        def __init__(self, path: str, data_name: str):
            self.path = path
            self.var_name = data_name
            self.init_dataset()
    '''

    def __post_init__(self):
        # lats: np.ma.core.MaskedArray
        # lons: np.ma.core.MaskedArray
        # time: np.ma.core.MaskedArray
        # # data: np.ma.core.MaskedArray  to be used to build an external database
        # min: np.ma.core.MaskedArray
        # max: np.ma.core.MaskedArray
        # median: np.ma.core.MaskedArray
        # var: np.ma.core.MaskedArray

        data_grp = Dataset(self.path)

        self.lats = data_grp.variables['lat'][:]
        self.lons = data_grp.variables['lon'][:]
        self.time = data_grp.variables['time'][:]
        data = data_grp.variables[self.var_name][:]

        self.min = data.min(axis=0)
        self.max = data.max(axis=0)
        self.median = np.ma.median(data, axis=0)
        self.var = data.var(axis=0)

        data_grp.close()

    def vectorize(self, array):
        '''
        Drops masked data and vectorizes data from our map arrays

        Args:
            array:

        Returns: 1-d np. array

        '''

        return


    def append_dataset(self, new_path):
        self.path = new_path

        data_grp = Dataset(self.path)

        new_time = data_grp.variables['time'][:]
        data = data_grp.variables[self.var_name][:]

        data_grp.close()

        self.min = np.concatenate((data.min(axis=0), self.min), axis=0).min(axis=0)
        self.max = np.concatenate((data.max(axis=0), self.max), axis=0).max(axis=0)
        self.median = np.concatenate((data.median(axis=0), self.median), axis=0).median(axis=0)
        self.var = np.concatenate((data.var(axis=0), self.median), axis=0).var(axis=0)
        self.time = np.concatenate((self.time, new_time), axis=0)


    def data_single_loc(self, lat_n, lon_n):

        stats = {}

        if np.ma.is_masked(self.data[:, lat_n, lon_n]):
            return False

        t_bin = self.data[:, lat_n, lon_n].data

        stats['lat'] = self.lats[lat_n]
        stats['lon'] = self.lons[lon_n]
        stats['min'] = min(t_bin)
        stats['max'] = max(t_bin)
        stats['std'] = np.std(t_bin)
        stats['mean'] = np.mean(t_bin)

        return stats

    def find_subset(self, lat_max, lat_min, lon_max, lon_min):

        select_lats = np.argwhere((self.lats > lat_min) & (self.lats < lat_max))
        select_lons = np.argwhere((self.lons > lon_min) & (self.lons < lon_max))

        return self.data[:, select_lats, select_lons]


if __name__ == "__main__":

    sets = dict()

    files = {'temp_max':    "C:\\Datasets\\Weather Data\\Copernicus\\Temp Max\\tasmaxAdjust_day_GFDL-ESM2G_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20160101-20201231.nc",
            'temp_min':     "C:\\Datasets\\Weather Data\\Copernicus\\Temp Mean\\tasAdjust_day_GFDL-ESM2G_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20160101-20201231.nc",
            'temp_mean':    "C:\\Datasets\\Weather Data\\Copernicus\\Temp Min\\tasminAdjust_day_GFDL-ESM2G_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20160101-20201231.nc",
            'precip':       "C:\\Datasets\\Weather Data\\Copernicus\\Precip Flux\\prAdjust_day_GFDL-ESM2G_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20160101-20201231.nc"
             }
    var_names = {'temp_max':  'tasmaxAdjust',
                 'temp_min':  'tasminAdjust',
                 'temp_mean': 'tasAdjust',
                 'precip':    'prAdjust'}

    # T_max_data = NCSet(temp_max_file, variable)

    for key, value in files.items():

        sets[key] = NCSet(value, var_names[key])

    with open('processed_weather_data.pickle', 'wb') as f:
        pickle.dump(sets, f)


    #temp_max_file = "C:\Data\Weather Data\Temp Max\\tasmaxAdjust_day_GFDL-ESM2M_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20010101-20051231.nc"
    #temp_min_file = "C:\Data\Weather Data\Temp Min\\tasminAdjust_day_GFDL-CM3_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20000101-20041231.nc"
    # temp_max_file = "C:\\Datasets\\Weather Data\\Copernicus\\Temp Max\\tasmaxAdjust_day_GFDL-ESM2G_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20160101-20201231.nc"
    # temp_mean_file = "C:\\Datasets\\Weather Data\\Copernicus\\Temp Mean\\tasAdjust_day_GFDL-ESM2G_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20160101-20201231.nc"
    # temp_min_file = "C:\\Datasets\\Weather Data\\Copernicus\\Temp Min\\tasminAdjust_day_GFDL-ESM2G_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20160101-20201231.nc"
    # precip_flux_file = "C:\\Datasets\\Weather Data\\Copernicus\\Precip Flux\\prAdjust_day_GFDL-ESM2G_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20160101-20201231.nc"
    # tmax_name = 'tasmaxAdjust'
    # tmin_name = 'tasminAdjust'
    # tm_name = 'tasAdjust'
    # precip_name = 'prAdjust'
    # print(timeit_loop(T_max_data))
    # print(timeit_loop(T_max_data))