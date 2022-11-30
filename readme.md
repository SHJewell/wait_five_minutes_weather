This project is meant to assess the statement "If you
don't like the weather, wait five minutes." It will use gelocated
weather averages and examine the likelyhood of rapid changes in
temperature, precipitation, wind, cloud cover and humidity.

Data is from Copernicus Atmospheric Monitoring Service (CAMS)
based in the EU. They can be found
https://atmosphere.copernicus.eu/

CAMS has a web API for pulling data directly into Python. Useful, that.

Pygrib really doesn't want to install on Windows, so we're
going to try cfgrib instead

First, we need to test the sizes and speeds of downloading various location and the
ability to dynamically find data. How fast can we do? How much can we grab?

Next we need to determine (or let the user determine) what we mean by variablility.
Chance of changes in extremes? Averages? Temperature? Pressure? Precipitation?

Structure:
The nc_set dataclass will contain the masked arrays of statistical analysis of the whole dataset.
If time permits, a SQL database can be set up to hold the raw data for the users edification,
but both the analysis and dashboard should be set up ahead of time.

Current path:
    Develop analysis
        Optional -- Path structure
        Optional -- Path decomposition
            Both of these could employ the C++ script writen
        mins
        maxes
        stds
        vars
        Combining the above
        What to keep in variables?
        How to store?
        Combine into dataclass
    Develop dashboard
        How much data to import at a time?
        Mapping
            Tiling
            Data selection methods
    Optional
        Additional data

