"""
Map data obtained from https://www.naturalearthdata.com/downloads/10m-cultural-vectors/
Full exact link: https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries.zip
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import bokeh.plotting as bkp
import geopandas as gp
from shapely.geometry import Point

# Loading the files
cwd = Path.cwd()
cwd = cwd.resolve(strict=True)
station_geocodes_file = cwd.joinpath("data","weather","SRCE.csv")
proj_file = cwd.joinpath("data","maps","ne_10m_admin_0_countries.dbf") # projection file, or the map that the coordinates will be projected onto
# proj_file_list = sorted(cwd.joinpath("data","maps").glob("*.shp"))

# Convert to a dataframe
df = pd.read_csv(station_geocodes_file)
# Create a "coordinates" column based on longitude & latitude
df['coordinates'] = list(zip(df.high_prcn_lon, df.high_prcn_lat))
# Turn into a point object
df['coordinates'] = df['coordinates'].apply(Point)
# Create a GeoDataFrame
gdf = gp.GeoDataFrame(df, geometry='coordinates')
# Assign "world" to the projection that we want
world = gp.read_file(proj_file)

# Plots the map
ax = world.plot(color='white', edgecolor='black')
# Sets the bounding box of the figure created
minx, miny, maxx, maxy = gdf.total_bounds
ax.set_xlim(minx-3, maxx+3)
ax.set_ylim(miny-3, maxy+3)
# Plots the GeoDataFrame
gdf.plot(ax=ax, color='red')
plt.show()

# for file in proj_file_list:
