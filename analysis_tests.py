
import xarray as xr
import numpy as np
import struct
from netCDF4 import Dataset
from matplotlib import pyplot as plt


# temp_max_file = "E:\\Documents\\Datasets\\Weather Data\\Temp Max\\tasmaxAdjust_day_GFDL-ESM2M_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20010101-20051231.nc"
# temp_min_file = "E:\\Documents\\Datasets\\Weather Data\\Temp Min\\tasminAdjust_day_GFDL-CM3_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20000101-20041231.nc"
temp_max_file = "C:\Data\Weather Data\Temp Max\\tasmaxAdjust_day_GFDL-ESM2M_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20010101-20051231.nc"
temp_min_file = "C:\Data\Weather Data\Temp Min\\tasminAdjust_day_GFDL-CM3_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20000101-20041231.nc"

t_min_grp = Dataset(temp_max_file)

lats = t_min_grp.variables['lat'][:]
lons = t_min_grp.variables['lon'][:]
time = t_min_grp.variables['time'][:]
t_mins = t_min_grp.variables['tasmaxAdjust'][:]

sea_lats = np.argwhere((lats > 46) & (lats < 47))
sea_lons = np.argwhere((lons > 122) & (lons < 123))
sea_tmins = t_mins[:, sea_lats, sea_lons].data


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
