
import xarray as xr
import numpy as np
import struct
from netCDF4 import Dataset
from matplotlib import pyplot as plt
import pandas as pd
import os
import dateutil.parser as parser
from dataclasses import dataclass
import datetime

'''
@dataclass
class MapLayer:
    var: str
    d_start: datetime.date
    d_end: datetime.date
    lat: 
    lon:
    layer_min:
    layer_max:
    mayer_std:
'''


file_directory_external = f"E:\\Documents\\Coding\\wait_five_minutes_weather\\nc_file_directory.csv"

file_directory = pd.read_csv(file_directory_external, index_col=False)

cols = file_directory.columns.tolist()

for folder in file_directory['folder'].unique().tolist():

    this_folder = file_directory[file_directory['folder'] == folder]
    date_start = datetime.date(1970, 1, 1)
    date_end = datetime.datetime.now().date()

    for file in this_folder['path']:

        if file[file.find('.'):] != '.nc':
            continue

        bits = file.split(os.sep)

        if parser.parse(bits[-1][-20:-12]) < date_start:
            date_start = parser.parse(bits[-1][-20:-12])

        if date_end > parser.parse(bits[-1][-11:-3]):
            date_end = parser.parse(bits[-1][-11:-3])

        data = Dataset(file)
        lat = data.variables['lat'][:]

        print(bits[-2], bits[-1])


    def random_coords(lats, lons):

        return np.random.choice(lats), np.random.choice(lons)


    def timeit_loop(ds):

        lats = ds.lats
        lons = ds.lons
        stats = []

        for n in range(0, 100):

            # lat, lon = random_coords(lats[:-100], lons[:-100])

            point = ds.data_single_loc(np.random.choice(range(len(lats))), np.random.choice(range(len(lons))))

            if not point:
                continue

            stats.append(point)

        return stats


    def timeit_fnc(ds):

        lats = ds.lats
        lons = ds.lons
        stats = {}

        rn = np.random.choice(range(len(lats)))
        lat_min = lats[rn]
        lat_max = lats[rn + 100]
        stats['lat'] = lats[rn:rn + 100]

        rn = np.random.choice(range(len(lons)))
        lon_min = lons[rn]
        lon_max = lons[rn + 100]
        stats['lon'] = lons[rn:rn + 100]

        dset = ds.find_subset(lat_max, lat_min, lon_max, lon_min)

        stats['min'] = dset.min(axis=0)
        stats['max'] = dset.max(axis=0)
        stats['std'] = dset.std(axis=0)
        stats['mean'] = dset.mean(axis=0)

        return stats

    #print(row['folder'], row['file'].split('_')[0])
    #print(row, type(row))

# temp_max_file = "E:\\Documents\\Datasets\\Weather Data\\Temp Max\\tasmaxAdjust_day_GFDL-ESM2M_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20010101-20051231.nc"
# temp_min_file = "E:\\Documents\\Datasets\\Weather Data\\Temp Min\\tasminAdjust_day_GFDL-CM3_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20000101-20041231.nc"
# temp_max_file = "C:\Data\Weather Data\Temp Max\\tasmaxAdjust_day_GFDL-ESM2M_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20010101-20051231.nc"
# temp_min_file = "C:\Data\Weather Data\Temp Min\\tasminAdjust_day_GFDL-CM3_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20000101-20041231.nc"

# t_min_grp = Dataset(temp_max_file)
#
# lats = t_min_grp.variables['lat'][:]
# lons = t_min_grp.variables['lon'][:]
# time = t_min_grp.variables['time'][:]
# t_mins = t_min_grp.variables['tasmaxAdjust'][:]
#
# sea_lats = np.argwhere((lats > 46) & (lats < 47))
# sea_lons = np.argwhere((lons > 122) & (lons < 123))
# sea_tmins = t_mins[:, sea_lats, sea_lons].data
#
# type(sea_lats)
#
# def gen_processes(path):


# N = len(sea_tmins)
# t_norm = time.max() - time.min()
# T = 1 / t_norm
# tx = np.linspace(0, N*T, N)
# xf = np.linspace(0.0, 1.0//(2.0*T), N//2)
# ft = np.fft.fft(sea_tmins)
# fig, ax = plt.subplots(3, 1)
#
# ax[0].plot(sea_tmins[:, 0, :], label=sea_lats[0])
# ax[0].plot(sea_tmins[:, 1, :], label=sea_lats[1])
# ax[1].plot(abs(sea_tmins[:, 0, :] - sea_tmins[:, 1, :]), label='Diff')
# ax[2].plot(xf, np.real(ft[:-len(xf), 0, :]), label=f'{sea_lats[0][0]}')
# ax[2].plot(xf, np.real(ft[:-len(xf), 1, :]), label=f'{sea_lats[1][0]}')
#
# plt.legend()
# plt.show()
#
# t_min_grp
