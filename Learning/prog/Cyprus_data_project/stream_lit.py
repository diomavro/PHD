import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# Display the current working directory
st.write("Current Working Directory:", os.getcwd())

# Load the data
df_gdp = pd.read_csv('streamlit_gdp.csv')

# Title of the app
st.title("GDP Growth vs GDP Plot")

# Sidebar for filtering options
st.sidebar.header("Filter Options")
entities = df_gdp['Entity'].unique()
selected_entities = st.sidebar.multiselect("Select Entities:", entities, default=entities)

# Filter data based on user selection
filtered_data = df_gdp[df_gdp['Entity'].isin(selected_entities)]

# Plotting the first plot
fig, ax = plt.subplots()

# Plot all points
ax.scatter(filtered_data['ln_rgdpo'], filtered_data['gdp_growth'], alpha=0.7, label='Data Points')

# Highlight and put on top points for Cyprus
cyprus_data = filtered_data[filtered_data['Entity'] == 'Cyprus']
ax.scatter(cyprus_data['ln_rgdpo'], cyprus_data['gdp_growth'], color='red', edgecolor='black', s=100, zorder=5,
           label='Cyprus')

# Compute the regression line
x = filtered_data['ln_rgdpo']
y = filtered_data['gdp_growth']
m, b = np.polyfit(x, y, 1)
ax.plot(x, m * x + b, color='blue', label=f'Regression Line: y = {m:.2f}x + {b:.2f}', zorder=4)

# Add labels, title, and legend
ax.set_title('GDP Growth vs Log(GDP)')
ax.set_xlabel('Log(GDP)')
ax.set_ylabel('GDP Growth')
ax.set_ylim(-0.1, 0.1)  # Set y-axis limits
ax.grid(True)
ax.legend()
# Display plot in Streamlit
st.pyplot(fig)

# Display the slope on the sidebar
st.sidebar.header("Regression Line Info")
st.sidebar.write(f"Slope (m): {m:.2f}")
st.sidebar.write(f"Intercept (b): {b:.2f}")

# Calculating the average log GDP growth per year
df_gdp['year'] = pd.to_datetime(df_gdp['Year'], format='%Y')
df_gdp['year'] = df_gdp['year'].dt.year
average_log_growth_per_year = df_gdp.groupby('Year')['gdp_growth'].mean().reset_index()

# Plotting the second plot
fig2, ax2 = plt.subplots()
ax2.scatter(average_log_growth_per_year['Year'], average_log_growth_per_year['gdp_growth'], alpha=0.7,
            label='Average Log Growth per Year')

# Highlight and put on top points for Cyprus in the second plot
cyprus_years = df_gdp[df_gdp['Entity'] == 'Cyprus']
cyprus_avg_log_growth = cyprus_years.groupby('Year')['gdp_growth'].mean().reset_index()
ax2.scatter(cyprus_avg_log_growth['Year'], cyprus_avg_log_growth['gdp_growth'], color='red', edgecolor='black', s=50,
            zorder=5, label='Cyprus')
ax2.plot(cyprus_avg_log_growth['Year'], cyprus_avg_log_growth['gdp_growth'], color='red', linestyle=':', linewidth=1.5,
         label='Cyprus Trend')

# Compute the regression line for the second plot
x2 = average_log_growth_per_year['Year']
y2 = average_log_growth_per_year['gdp_growth']
m2, b2 = np.polyfit(x2, y2, 1)
ax2.plot(x2, m2 * x2 + b2, color='blue', label=f'Regression Line: y = {m2:.2f}x + {b2:.2f}')

# Add labels, title, and legend
ax2.set_title('Average Log Growth per Year')
ax2.set_xlabel('Year')
ax2.set_ylabel('Average Log Growth')
ax2.grid(True)
ax2.legend()

# Display second plot in Streamlit
st.pyplot(fig2)

# streamlit run /home/dio/Documents/PHD/Learning/prog/Cyprus_data_project/stream_lit.py
