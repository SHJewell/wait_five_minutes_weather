
from netCDF4 import Dataset
import numpy as np
import datetime
import calendar

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

new_data = {'mean':     '',
            'median':   ''}


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

def reduce_to_month_single(files, new_file, start_date, end_date):

    extracted_sets = list(files.keys())
    rootgrp = Dataset(files[extracted_sets[0]], 'r')

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

        # rootgrp = Dataset(files[var_name], 'r')
        # dset = rootgrp.variables[var_name][days_diff[0]:days_diff[1], :, :]
        # rootgrp.close()
        #
        # new_var = newgrp.createVariable(var_name, 'f4', ('time', 'lat', 'lon'))
        # new_var[:,:,:] = dset
        # newgrp.sync()

    newgrp.close()

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
    #new_file = "/data/Means-GFDL-ESM2G_SMHI-postproc-20010101-20051231.nc"
    new_file = "/home/shjewell/PycharmProjects/basic_geo_dashboard/data/master_20010101-20010201.nc"

    #procfile = newNCFile()
    #reduce_to_month_multi(files, new_files)

    start_date = datetime.date(year=2001, month=1, day=1)
    end_date = datetime.date(year=2001, month=2, day=1)

    reduce_to_month_single(files, new_file, start_date, end_date)