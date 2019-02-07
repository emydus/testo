import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import bokeh.plotting as bkp
import geopandas as gp
from shapely.geometry import Point

cwd = Path.cwd()
cwd = cwd.resolve(strict=True)
station_geocodes_file = cwd.joinpath("data","weather","SRCE.csv")
proj_file = cwd.joinpath("data","maps","europe-latest.osm.pbf")
proj_file_list = sorted(cwd.joinpath("data","maps").glob("*.shp"))

df = pd.read_csv(station_geocodes_file)
df['coordinates'] = list(zip(df.high_prcn_lon, df.high_prcn_lat))
df['coordinates'] = df['coordinates'].apply(Point)
gdf = gp.GeoDataFrame(df, geometry='coordinates')
world = gp.read_file(proj_file)

ax = world.plot(color='white', edgecolor='black')
minx, miny, maxx, maxy = gdf.total_bounds
ax.set_xlim(minx-3, maxx+3)
ax.set_ylim(miny-3, maxy+3)

# We can now plot our GeoDataFrame.
gdf.plot(ax=ax, color='red')

plt.show()

#for file in proj_file_list:
#    

