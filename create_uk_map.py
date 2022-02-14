import numpy as np
import pandas as pd
from matplotlib import colors
from matplotlib import cm
import matplotlib.pyplot as plt
import geopandas as gpd

df=pd.read_csv('Uk_map')

D={'blue': [(0.0, 0, 0), (0.75, 0.75, 0.75)],
 'green': [(0.0, 0, 0), (0.75, 0.75, 0.75)],
 'red': [(0.0, 0, 0), (0.75, 0.75, 0.75)]}

for item in ['blue', 'green', 'red']:
    seg=np.linspace(0,1,len(D[item]))
    for i in range(len(D[item])):
        D[item][i]=(seg[i],D[item][i][1],D[item][i][2]) 

New_cm = colors.LinearSegmentedColormap('New_cm', D)

# initialize an axis
fig, ax = plt.subplots(figsize=(8,6))
# plot map on axis
countries = gpd.read_file(  
     gpd.datasets.get_path("naturalearth_lowres"))
countries[countries["name"] == "United Kingdom"].plot(color="white",
                                                 ax=ax)
# parse dates for plot's title

# plot points
df.plot(x="longitude", y="latitude", kind="scatter", 
        c="brai", colormap=New_cm,ax=ax, colorbar=False, s=1)

plt.axis('off')

# add grid
#ax.grid(b=True, alpha=0.5)
#plt.show()
plt.savefig('uk_map')
