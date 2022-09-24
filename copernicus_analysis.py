import numpy as np
from netCDF4 import Dataset
import timeit

class nc_set():
    def __init__(self, path, data_name):
        self.path = path
        self.var_name = data_name
        self.init_dataset()

    def init_dataset(self):
        data_grp = Dataset(self.path)

        self.lats = data_grp.variables['lat'][:]
        self.lons = data_grp.variables['lon'][:]
        self.time = data_grp.variables['time'][:]
        self.data = data_grp.variables[self.var_name][:]

        data_grp.close()

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
    lat_max = lats[rn+100]
    stats['lat'] = lats[rn:rn+100]

    rn = np.random.choice(range(len(lons)))
    lon_min = lons[rn]
    lon_max = lons[rn+100]
    stats['lon'] = lons[rn:rn+100]

    dset = ds.find_subset(lat_max, lat_min, lon_max, lon_min)

    stats['min'] = dset.min(axis=0)
    stats['max'] = dset.max(axis=0)
    stats['std'] = dset.std(axis=0)
    stats['mean'] = dset.mean(axis=0)

    return stats


if __name__ == "__main__":

    temp_max_file = "C:\Data\Weather Data\Temp Max\\tasmaxAdjust_day_GFDL-ESM2M_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20010101-20051231.nc"
    temp_min_file = "C:\Data\Weather Data\Temp Min\\tasminAdjust_day_GFDL-CM3_SMHI-DBSrev930-GFD-1981-2010-postproc_rcp45_r1i1p1_20000101-20041231.nc"
    variable = 'tasmaxAdjust'

    T_max_data = nc_set(temp_max_file, variable)

    print(timeit.Timer('timeit_loop(ds)').timeit(number=100))
    print(timeit.Timer('timeit_fnc(ds)').timeit(number=100))

    # print(timeit_loop(T_max_data))
    # print(timeit_loop(T_max_data))