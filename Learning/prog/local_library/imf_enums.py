import requests
import pandas as pd
import enum
import re


def sanitize_name(name):
    # Replace invalid characters with underscores
    name = re.sub(r'\W|^(?=\d)', '_', name)
    return name


# Function to fetch the IMF indicators and create the enum class
def omega_imf():
    # Define the API URL for indicators
    url = 'https://www.imf.org/external/datamapper/api/v1/indicators'

    # Send a GET request to the API URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the data options (Assuming they are in the 'indicators' key)
        data_options = data['indicators'].keys()

        # Filter out empty keys and sanitize the names
        sanitized_options = {sanitize_name(option): option for option in data_options if option}

        # Create an enum class dynamically
        DataOptionsEnum = enum.Enum('DataOptionsEnum', sanitized_options)

        return DataOptionsEnum
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None


# Function to get data from the IMF using the enum
def get_imf_data(data_option):
    # Define the base API URL
    base_url = 'https://www.imf.org/external/datamapper/api/v1/'

    # Construct the full API URL using the enum value
    url = f'{base_url}{data_option.value}'

    # Send a GET request to the API URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Convert the JSON data to a pandas DataFrame
        df = pd.DataFrame(data['values'])

        # Melt the DataFrame
        melted_data = []
        for country, values in df.iterrows():
            for date, value in values[0].items():
                melted_data.append([country, date, value])

        melted_df = pd.DataFrame(melted_data, columns=['Country', 'Date', data_option.name])

        return melted_df
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None


if __name__ == '__main__':
    print('hello')
    DataOptionsEnum = omega_imf()

    if DataOptionsEnum:
        # Example: Fetch data for the first available indicator
        df = get_imf_data(DataOptionsEnum.NGDP_RPCH)  # Replace with your desired enum member

        if df is not None:
            print(df.head())
