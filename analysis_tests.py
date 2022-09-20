
import xarray as xr
import numpy as np
import struct
from netCDF4 import Dataset
from matplotlib import pyplot as plt


temp_max_file = "E:\\Documents\\Datasets\\Weather Data\\Temp Max\\tasmaxAdjust_day_GFDL-ESM2M_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20010101-20051231.nc"
temp_min_file = "E:\\Documents\\Datasets\\Weather Data\\Temp Min\\tasminAdjust_day_GFDL-CM3_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20000101-20041231.nc"
t_min_grp = Dataset(temp_max_file)

lats = t_min_grp.variables['lat'][:]
lons = t_min_grp.variables['lon'][:]
time = t_min_grp.variables['time'][:]
t_mins = t_min_grp.variables['tasmaxAdjust'][:]

sea_lats = np.argwhere((lats > 46) & (lats < 47))
sea_lons = np.argwhere((lons > 122) & (lons < 123))
sea_tmins = t_mins[:, sea_lats, sea_lons].data

fig, ax = plt.subplots()

ax.plot(sea_tmins[:, 0, :])
ax.plot(sea_tmins[:, 1, :])

plt.show()

t_min_grp
