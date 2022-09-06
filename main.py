import cfgrib
import xarray as xr
import pandas as pd
import numpy as np
from osgeo import gdal
import struct
from netCDF4 import Dataset

from matplotlib import pyplot as plt

'''
netcdf4 excecise
'''

def walktree(top):
    yield top.groups.values()
    for value in top.groups.values():
        yield from walktree(value)

rootgrp = Dataset('E:\Documents\Datasets\Weather Data\\tasminAdjust_day_GFDL-CM3_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20000101-20041231.nc')

# for children in walktree(rootgrp):
#     for child in children:
#         print(child)

for name in rootgrp.ncattrs():
    print(f'Global attr {getattr(rootgrp, name)}')

print(rootgrp.data_model)
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


