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