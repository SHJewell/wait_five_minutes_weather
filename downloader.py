
import cdsapi
'''
Datasets:

    METAR:
    https://mesonet.agron.iastate.edu/request/download.phtml?network=WA_ASOS
    
    ISD:
    https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database

    Copernicus data:
    Has an API but is somewhat persnickety without a list of explicit sets desired.
    
    Essentials: Max temp, Min temp, Mean temp an Precipitation flux:
    https://cds.climate.copernicus.eu/cdsapp#!/dataset/sis-ecv-cmip5-bias-corrected?tab=overview

    Precipitation:
    https://cds.climate.copernicus.eu/cdsapp#!/dataset/satellite-precipitation?tab=overview

    Pressure:
    https://cds.climate.copernicus.eu/cdsapp#!/dataset/projections-cmip5-daily-pressure-levels?tab=overview
    
    Humidity:
    https://cds.climate.copernicus.eu/cdsapp#!/dataset/satellite-upper-troposphere-humidity?tab=overview
    
    Wind:
    https://cds.climate.copernicus.eu/cdsapp#!/dataset/insitu-observations-gruan-reference-network?tab=overview
    
    Sunshine/cloudcover:
    https://cds.climate.copernicus.eu/cdsapp#!/dataset/satellite-earth-radiation-budget?tab=overview

    Maybe use the MERRA-2 data?
    https://disc.gsfc.nasa.gov/datasets?project=MERRA-2

'''


# example:
c = cdsapi.Client()
# c.retrieve("reanalysis-era5-pressure-levels",
#     {
#     "variable": "temperature",
#     "pressure_level": "1000",
#     "product_type": "reanalysis",
#     "year": "2008",
#     "month": "01",
#     "day": "01",
#     "time": "12:00",
#     "format": "grib"
#     }, "download.grib")

c.retrieve(
    'sis-ecv-cmip5-bias-corrected',
    {
        'format': 'zip',
        'variable': 'minimum_2m_temperature',
        'period': '20000101-20041231',
        'experiment': 'rcp_4_5',
        'model': 'gfdl_cm3',
    },
    'download.zip')

dir(c)