import pandas as pd
import enum

data = r'/home/dio/Documents/PHD/Learning/prog/Cyprus_data_project/streamlit_gdp.csv'

df = pd.read_csv(data)

# Extract unique values from the 'entity' column
unique_entities = df['Entity'].unique()

# Create an enum class dynamically
EntityEnum = enum.Enum('EntityEnum', {entity: entity for entity in unique_entities})

# Print the enum class members
for entity in EntityEnum:
    print(entity)

