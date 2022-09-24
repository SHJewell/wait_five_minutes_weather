#import cfgrib
import xarray as xr
import pandas as pd
import numpy as np
#from osgeo import gdal
import struct
from netCDF4 import Dataset

from matplotlib import pyplot as plt
import mpl_toolkits
from mpl_toolkits.basemap import Basemap

'''
netcdf4 excecise
'''

def walktree(top):
    yield top.groups.values()
    for value in top.groups.values():
        yield from walktree(value)

# E:\\Documents\\Datasets\\Weather Data\\Temp Max\\tasmaxAdjust_day_GFDL-ESM2M_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20010101-20051231.nc"
t_min_grp = Dataset("E:\\Documents\\Datasets\\Weather Data\\Temp Min\\tasminAdjust_day_GFDL-CM3_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20000101-20041231.nc")

# for children in walktree(t_min_grp):
#     for child in children:
#         print(child)

# for name in t_min_grp.ncattrs():
#     print(f'Global attr {getattr(t_min_grp, name)}')

lats = t_min_grp.variables['lat'][:]
lons = t_min_grp.variables['lon'][:]
t_mins = t_min_grp.variables['tasminAdjust'][:]
temp_units = t_min_grp.variables['tasminAdjust'].units

t_min_grp.close()

lon0 = lons.mean()
lat0 = lats.mean()

# this is for mapping... which might work?
#m = Basemap(width=8000000, height=3500000, resolution='l', projection='stere', lat_ts=40, lat_0=lat0, lon_0=lon0)
m = Basemap(width=12000000, height=9000000, resolution='l', projection='lcc', lat_1=45., lat_2=55, lat_0=50, lon_0=-107)

lon, lat = np.meshgrid(lons, lats)
xi, yi = m(lon, lat)

# Plot data
cs = m.pcolor(xi, yi, np.squeeze(t_mins[0]))

# Add grid lines
m.drawparallels(np.arange(-80., 81., 10.), labels=[1, 0, 0, 0], fontsize=10)
m.drawparallels(np.arange(-180., 181., 10.), labels=[0, 0, 0, 1], fontsize=10)

# Add coastlines, states and country boundaries
m.drawcoastlines()
m.drawstates()
m.drawcountries()

# Add colorbar
cbar = m.colorbar(cs, location='bottom', pad='10%')
cbar.set_label(temp_units)

# add title
plt.title('DJF Maximum Temperature')

plt.show()
print(t_min_grp.data_model)
'''
netcdf4 excecise
'''

'''
osgeo-gdal excercise
'''

# dataset = gdal.Open("E:\Documents\Datasets\Weather Data\\tasminAdjust_day_GFDL-CM3_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20000101-20041231.nc",
#                     gdal.GA_ReadOnly)
# if not dataset:
#     ...
#
# print(f'Driver: {dataset.GetDriver().ShortName}/{dataset.GetDriver().LongName}')
# print(f'Size is {dataset.RasterXSize} x {dataset.RasterYSize} x {dataset.RasterCount}')
# print(f'Projection is {dataset.GetProjection()}')
# geotransform = dataset.GetGeoTransform()
# if geotransform:
#     print(f'Origin = ({geotransform[0]}, {geotransform[3]}')
#     print(f'Pixel Size = ({geotransform[1]}, {geotransform[5]}')
#
# band = dataset.GetRasterBand(1)
# print(f'Band Type={gdal.GetDataTypeName(band.DataType)}')
#
# min = band.GetMinimum()
# max = band.GetMaximum()
#
# if not min or not max:
#     (min, max) = band.ComputeRasterMinMax(True)
# print(f'Min={min:.3f}, Max={max:.3f}')
#
# if band.GetOverviewCount() > 0:
#     print(f'Band has {band.GetOverviewCount()} overviews')
#
# if band.GetRasterColorTable():
#     print(f'Band has a color table with {band.GetRasterColorTable().GetCount()} entries')
#
# scanline = band.ReadRaster(xoff=0, yoff=0,
#                         xsize=band.XSize, ysize=1,
#                         buf_xsize=band.XSize, buf_ysize=1,
#                         buf_type=gdal.GDT_Float32)
#
# tuple_of_floats = struct.unpack('f' * band.XSize, scanline)
#
# dir(dataset)

'''
osgeo-gdal excercise
'''

'''
xarray excercise
'''
# ds = xr.open_dataset('download.grib', engine='cfgrib')
#
# ds

# data_path = "E:\Documents\Datasets\Weather Data\\adaptor.mars.internal.grib"
# test_path = "E:\Documents\Datasets\Test Sets\era5-levels-members.grib"
#
# ds = xr.open_dataset(data_path, engine='cfgrib')
# test_set = xr.open_dataset(test_path, engine='cfgrib')
#
# test_set
# ds
'''
xarray excercise
'''


