import numpy as np

from netCDF4 import Dataset
from dataclasses import dataclass
import pickle
import sys
import tracemalloc
import datetime
import scipy

@dataclass
class NCSet:
    path: str
    var_name: str

    def __post_init__(self):
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

def wait_five_minutes_analysis(files, new_file, start_date=None, end_date=None):
    '''
    Analysis needed:
        *Daily temperature swing
        *Precipitation standard deviation
        *variability in temperature (standard deviation?)
        *liklihood of it getting much cooler
        *liklihood of it getting much warmer
    Returns:

    '''


    extracted_sets = list(files.keys())
    rootgrp = Dataset(files[extracted_sets[0]], 'r')

    new_file = f'{new_file}-{start_date.strftime("%Y%m%d")}-{end_date.strftime("%Y%m%d")}.nc'
    date0 = datetime.timedelta(days=np.floor(float(rootgrp.variables['time'][0]))) + datetime.date(year=1850,
                                                                                                   month=1, day=1)
    days_diff = []
    days_diff.append((start_date - date0).days)
    days_diff.append((end_date - date0).days)

    lats = rootgrp.variables['lat'][:]
    lons = rootgrp.variables['lon'][:]
    dt = rootgrp.variables['time'][days_diff[0]:days_diff[1]]
    dset = rootgrp.variables[extracted_sets[0]][days_diff[0]:days_diff[1], :, :]

    newgrp = Dataset(new_file, "w")
    newgrp.createDimension('lat', len(lats))
    newgrp.createDimension('lon', len(lons))
    newgrp.createDimension('time', len(dt))
    lat = newgrp.createVariable('lat', 'f4', ('lat',))
    lat[:] = lats
    lon = newgrp.createVariable('lon', 'f4', ('lon',))
    lon[:] = lons

    for n, var_name in enumerate(extracted_sets):
        print(var_name)

        if n != 0:
            rootgrp = Dataset(files[extracted_sets[n]], 'r')
            dset = rootgrp.variables[extracted_sets[n]][days_diff[0]:days_diff[1], :, :]

        new_var_mean = newgrp.createVariable(f'{var_name}_mean', 'f4', ('lat', 'lon'))
        new_var_mean[:, :] = np.nanmean(dset, axis=0)
        new_var_median = newgrp.createVariable(f'{var_name}_median', 'f4', ('lat', 'lon'))
        new_var_median[:, :] = np.nanmedian(dset, axis=0)
        new_var_max = newgrp.createVariable(f'{var_name}_max', 'f4', ('lat', 'lon'))
        new_var_max[:, :] = np.max(dset, axis=0)
        new_var_min = newgrp.createVariable(f'{var_name}_min', 'f4', ('lat', 'lon'))
        new_var_min[:, :] = np.min(dset, axis=0)
        new_var_std = newgrp.createVariable(f'{var_name}_std', 'f4', ('lat', 'lon'))
        new_var_std[:, :] = np.nanstd(dset, axis=0)

    #temp_swing
    print('Temp Swing')
    temp_swing = newgrp.createVariable(f'temp_swing', 'f4', ('lat', 'lon'))
    temp_swing[:, :] = newgrp.variables['tasmaxAdjust_mean'][:] - newgrp.variables['tasminAdjust_mean'][:]

    #total temp variability
    print('Temp Variability')
    temp_variability = newgrp.createVariable(f'temp_var', 'f4', ('lat', 'lon'))
    temp_variability[:, :] = np.nanmean([newgrp.variables['tasmaxAdjust_std'][:],
                                        newgrp.variables['tasminAdjust_std'][:],
                                        newgrp.variables['tasAdjust_std'][:]], axis=0)

    #liklihood of hot day
    tdiff = np.diff(rootgrp.variables['tasmaxAdjust'][:] - np.nanmean(rootgrp.variables['tasAdjust'][:]))

    rootgrp.close()
    newgrp.sync()
    newgrp.close()

    def likelyhood_analysis():

        pass


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