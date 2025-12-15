import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Get the current working directory
current_directory = Path(os.getcwd())

parent_directory = Path(current_directory).parent
lib_dir = current_directory / 'local_library'

sys.path.append(parent_directory)
sys.path.append(current_directory)
sys.path.append(lib_dir)

from local_library.load_data import our_world_data

df_life, metadata_life, df_gdp, metadata_gdp = our_world_data(fetch=True)

df_gdp = df_gdp.sort_values(by=['Entity', 'Year'])
df_gdp['gdp_growth'] = df_gdp.groupby('Entity')['rgdpo'].pct_change().shift(-1)
df_gdp.dropna(inplace=True)
df_gdp['ln_rgdpo'] = np.log(df_gdp['rgdpo'])

df_gdp.to_csv('streamlit_gdp.csv')

# Plotting the data
plt.figure(figsize=(10, 6))
plt.scatter(df_gdp['rgdpo'], df_gdp['gdp_growth'], alpha=0.7)
plt.title('GDP Growth vs GDP')
plt.xlabel('GDP')
plt.ylabel('GDP Growth')
plt.grid(True)
plt.show()

print('hello')
