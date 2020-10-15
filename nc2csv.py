#!/usr/bin/python3

import netCDF4
from netCDF4 import num2date
import numpy as np
import os
import pandas as pd

file_location = './HadISST.2.1.0.0_realisation_69.nc'
# Open netCDF4 file
f = netCDF4.Dataset(file_location)

# Extract variable
sst = f.variables['sst']

# Get dimensions assuming 3D: time, latitude, longitude
time_dim, lat_dim, lon_dim = sst.get_dims()
time_var = f.variables[time_dim.name]
times = num2date(time_var[:], time_var.units)
latitudes = f.variables[lat_dim.name][:]
longitudes = f.variables[lon_dim.name][:]

output_dir = './'

# =====================================================================
# Write data as a table with 4 columns: time, latitude, longitude, value
# =====================================================================
output_csv = file_location.rsplit(".", 1)[0].split("/")[-1] + '.csv'
filename = os.path.join(output_dir, output_csv)
print(f'Writing data in tabular form to {filename} (this may take some time)...')
times_grid, latitudes_grid, longitudes_grid = [
    x.flatten() for x in np.meshgrid(times, latitudes, longitudes, indexing='ij')]
df = pd.DataFrame({
    'time': [t.isoformat() for t in times_grid],
    'latitude': latitudes_grid,
    'longitude': longitudes_grid,
    'sst': sst[:].flatten()})
df.to_csv(filename, index=False)
print('Done')
