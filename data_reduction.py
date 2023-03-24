
from netCDF4 import Dataset
import numpy as np
import datetime
import calendar

def reduce_to_month_multi(files, new_files):
    '''
    Reduces the amount of data per file along the time access, and saves each variable as its own set.

    '''

    days_diff = calendar.monthrange(2001, 1)
    extracted_sets = list(files.keys())

    for n, var_name in enumerate(extracted_sets):

        rootgrp = Dataset(files[var_name], 'r')
        lats = rootgrp.variables['lat'][:]
        lons = rootgrp.variables['lon'][:]
        dt = rootgrp.variables['time'][days_diff[0]:days_diff[1]]
        dset = rootgrp.variables[var_name][days_diff[0]:days_diff[1], :, :]
        rootgrp.close()

        newgrp = Dataset(new_files[var_name], "w")
        newgrp.createDimension('lat', len(lats))
        newgrp.createDimension('lon', len(lons))
        newgrp.createDimension('time', len(dt))
        t = newgrp.createVariable('time', 'f4', ('time',))
        t[:] = dt
        lon = newgrp.createVariable('lon', 'f4', ('lon',))
        lon[:] = lons
        lat = newgrp.createVariable('lat', 'f4', ('lat',))
        lat[:] = lats
        new_var = newgrp.createVariable(var_name, 'f4', ('time', 'lat', 'lon'))
        new_var[:,:,:] = dset
        newgrp.sync()

    newgrp.close()

def reduce_to_month_single(files, new_file, start_date, end_date, dt=1):
    '''
    Reduces the amount of data per file along the time access, and combines all the data into a single file

    '''

    extracted_sets = list(files.keys())
    rootgrp = Dataset(files[extracted_sets[0]], 'r')
    new_file = f'{new_file}-{start_date.strftime("%Y%m%d")}-{dt}-{end_date.strftime("%Y%m%d")}.nc'

    date0 = datetime.timedelta(days=np.floor(float(rootgrp.variables['time'][0]))) + datetime.date(year=1850, month=1, day=1)

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
    t = newgrp.createVariable('time', 'f4', ('time'))
    t[:] = dt

    for n, var_name in enumerate(extracted_sets):

        if n != 0:

            rootgrp = Dataset(files[extracted_sets[n]], 'r')

            if extracted_sets[n] not in rootgrp.variables.keys():
                print(f'{extracted_sets[n]} not in file!')
                exit()

            dset = rootgrp.variables[extracted_sets[n]][days_diff[0]:days_diff[1], :, :]

        new_var = newgrp.createVariable(var_name, 'f4', ('time', 'lat', 'lon'))
        new_var[:, :, :] = dset
        newgrp.sync()

    rootgrp.close()
    newgrp.close()

def whole_set_stats(files, new_file, start_date, end_date):
    '''
    Reduces the amount of data per file along the time access, and combines all the data into a single file

    '''

    extracted_sets = list(files.keys())
    rootgrp = Dataset(files[extracted_sets[0]], 'r')
    if extracted_sets[0] not in rootgrp.variables.keys():
        print(f'{extracted_sets[0]} not in file!')
        exit()
    new_file = f'{new_file}-{start_date.strftime("%Y%m%d")}-{end_date.strftime("%Y%m%d")}.nc'

    date0 = datetime.timedelta(days=np.floor(float(rootgrp.variables['time'][0]))) + datetime.date(year=1850, month=1, day=1)

    days_diff = []
    days_diff.append((start_date - date0).days)
    days_diff.append((end_date - date0).days)

    lats = rootgrp.variables['lat'][:]
    lons = rootgrp.variables['lon'][:]
    dt = rootgrp.variables['time'][days_diff[0]:days_diff[1]]
    dset = rootgrp.variables[extracted_sets[0]][days_diff[0]:days_diff[1], :, :]
    rootgrp.close()

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

            if extracted_sets[n] not in rootgrp.variables.keys():
                print(f'{extracted_sets[n]} not in file!')
                exit()

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
        newgrp.sync()

    newgrp.close()

def time_bin_stats(files, new_file, start_date, end_date, dt=1, t_unit='day'):
    '''
    Reduces the amount of data per file along the time access, and combines all the data into a single file

    '''

    extracted_sets = list(files.keys())
    rootgrp = Dataset(files[extracted_sets[0]], 'r')
    new_file = f'{new_file}-{start_date.strftime("%Y%m%d")}-{dt}-{end_date.strftime("%Y%m%d")}.nc'

    date0 = datetime.timedelta(days=round(float(rootgrp.variables['time'][0]))) + datetime.date(year=1850, month=1, day=1)

    days_diff = []
    days_diff.append((start_date - date0).days)
    days_diff.append((end_date - date0).days)

    lats = rootgrp.variables['lat'][:]
    lons = rootgrp.variables['lon'][:]
    dt = rootgrp.variables['time'][days_diff[0]:days_diff[1]]
    dset = rootgrp.variables[extracted_sets[0]][days_diff[0]:days_diff[1], :, :]
    rootgrp.close()

    newgrp = Dataset(new_file, "w")
    newgrp.createDimension('lat', len(lats))
    newgrp.createDimension('lon', len(lons))
    newgrp.createDimension('time', len(dt))
    lat = newgrp.createVariable('lat', 'f4', ('lat',))
    lat[:] = lats
    lon = newgrp.createVariable('lon', 'f4', ('lon',))
    lon[:] = lons
    t = newgrp.createVariable('time', 'f4', ('time'))
    t[:] = dt

    for n, var_name in enumerate(extracted_sets):

        if n != 0:
            rootgrp = Dataset(files[extracted_sets[0]], 'r')
            dset = rootgrp.variables[extracted_sets[0]][days_diff[0]:days_diff[1], :, :]

        new_var = newgrp.createVariable(var_name, 'f4', ('time', 'lat', 'lon'))
        new_var[:, :, :] = dset
        newgrp.sync()

    newgrp.close()

#def likelyhood_analysis():

class newNCFile:
    def __init__(self, filename, input_data):
        self.filename = filename
        self.input_data = input_data

        self.rootgrp = Dataset(
            list(input_data.keys())[0], 'r')
        self.lats = self.rootgrp.variables['lat'][:]
        self.lons = self.rootgrp.variables['lon'][:]

        self.rootgrp.variables.keys()
        self.rootgrp.close()




if __name__ == "__main__":
    files = {
        'tasmaxAdjust': "/media/disc1/Datasets/Weather Data/Copernicus/Temp Max/tasmaxAdjust_day_GFDL-ESM2G_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20010101-20051231.nc",
        'tasAdjust': "/media/disc1/Datasets/Weather Data/Copernicus/Temp Mean/tasAdjust_day_GFDL-ESM2G_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20010101-20051231.nc",
        'tasminAdjust': "/media/disc1/Datasets/Weather Data/Copernicus/Temp Min/tasminAdjust_day_GFDL-ESM2G_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20010101-20051231.nc",
        'prAdjust': "/media/disc1/Datasets/Weather Data/Copernicus/Precip Flux/prAdjust_day_GFDL-ESM2G_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20010101-20051231.nc"
    }

    new_files = {
        'tasmaxAdjust': "/home/shjewell/PycharmProjects/basic_geo_dashboard/data/tasmaxAdjust_20010101-20010201.nc",
        'tasAdjust': "/home/shjewell/PycharmProjects/basic_geo_dashboard/data/tasAdjust_20010101-20010201.nc",
        'tasminAdjust': "/home/shjewell/PycharmProjects/basic_geo_dashboard/data/tasminAdjust_20010101-20010201.nc",
        'prAdjust': "/home/shjewell/PycharmProjects/basic_geo_dashboard/data/prAdjust_20010101-20010201.nc"

    }

    files_q4 = {
        'tasminAdjust': '/media/disc1/Datasets/Weather Data/Copernicus/Temp Min/tasminAdjust_day_GFDL-ESM2G_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20160101-20201231.nc',
        'tasAdjust': '/media/disc1/Datasets/Weather Data/Copernicus/Temp Mean/tasAdjust_day_GFDL-ESM2G_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20160101-20201231.nc',
        'tasmaxAdjust': '/media/disc1/Datasets/Weather Data/Copernicus/Temp Max/tasmaxAdjust_day_GFDL-ESM2G_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20160101-20201231.nc',
        'prAdjust': '/media/disc1/Datasets/Weather Data/Copernicus/Precip Flux/prAdjust_day_GFDL-ESM2G_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20160101-20201231.nc'
    }

    files_small = {
        'tasAdjust': '/media/disc1/Datasets/Weather Data/Copernicus/Temp Mean/tasAdjust_day_GFDL-ESM2G_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20160101-20201231.nc',
        'prAdjust': '/media/disc1/Datasets/Weather Data/Copernicus/Precip Flux/prAdjust_day_GFDL-ESM2G_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20160101-20201231.nc'
    }

    new_data = {'mean': '',
                'median': ''}

    # new_file = "/data/Means-GFDL-ESM2G_SMHI-postproc-20010101-20051231.nc"
    new_file = "/home/shjewell/PycharmProjects/basic_geo_dashboard/data/master"
    # new_file = "/media/disc1/Datasets/Weather Data/Processed/stats"

    #procfile = newNCFile()
    #reduce_to_month_multi(files, new_files)

    start_date = datetime.date(year=2001, month=1, day=1)
    #end_date = datetime.date(year=2020, month=12, day=31)
    end_date = datetime.date(year=2005, month=12, day=31)

    #reduce_to_month_single(files_small, new_file, datetime.date(year=2020, month=1, day=1), datetime.date(year=2020, month=12, day=31))

    reduce_to_month_single(files, new_file, start_date, end_date)
    # reduce_to_month_single_average(files, new_file, start_date, end_date)
    # whole_set_stats(files, new_file, datetime.date(year=2001, month=1, day=1), datetime.date(year=2005, month=12, day=31))