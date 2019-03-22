import pandas as pd
import os
import geocoder
path = r'/Users/Eloisa/Google Drive/MWay_Comms'
csv = 'M42 Midas Outstations.csv'
file = os.path.join(path, csv)
df = pd.read_csv(file, usecols=['Latitude','Longitude','Geog. Address'])
lat = df['Latitude'][0] ; lon = df['Longitude'][0]
g = geocoder.bing([lat,lon], method='reverse')
print(g.postal)