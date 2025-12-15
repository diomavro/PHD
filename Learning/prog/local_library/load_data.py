import json
from io import StringIO

import pandas as pd
import pandas_datareader.data as web
import requests
import requests
import pandas as pd
from typing import List, Dict, Union, Optional


def our_world_data(fetch: bool = False):
    data_dir = '/home/dio/Documents/PHD/Learning/prog/data/'
    if fetch:
        df_life = pd.read_csv(
            "https://ourworldindata.org/grapher/life-expectancy.csv?v=1&csvType=full&useColumnShortNames=true",
            storage_options={'User-Agent': 'Our World In Data data fetch/1.0'})

        metadata_life = requests.get(
            "https://ourworldindata.org/grapher/life-expectancy.metadata.json?v=1&csvType=full&useColumnShortNames=true").json()

        df_gdp = pd.read_csv(
            "https://ourworldindata.org/grapher/national-gdp-penn-world-table.csv?v=1&csvType=full&useColumnShortNames=true",
            storage_options={'User-Agent': 'Our World In Data data fetch/1.0'})

        metadata_gdp = requests.get(
            "https://ourworldindata.org/grapher/national-gdp-penn-world-table.metadata.json?v=1&csvType=full&useColumnShortNames=true").json()

        df_life.to_csv(data_dir + 'df_life.csv', index=False)
        df_gdp.to_csv(data_dir + 'df_gdp.csv', index=False)

        with open(data_dir + 'metadata_life.json', 'w') as json_file:
            json.dump(metadata_life, json_file)
        with open(data_dir + 'metadata_gdp.json', 'w') as json_file:
            json.dump(metadata_gdp, json_file)

    else:
        df_life = pd.read_csv(data_dir + 'df_life.csv')
        df_gdp = pd.read_csv(data_dir + 'df_gdp.csv')

        with open(data_dir + 'metadata_life.json', 'r') as json_file:
            metadata_life = json.load(json_file)
        with open(data_dir + 'metadata_gdp.json', 'r') as json_file:
            metadata_gdp = json.load(json_file)

    return df_life, metadata_life, df_gdp, metadata_gdp


def get_oecd_private_consumption():
    # URL to the OECD data table
    # url = "https://www.oecd.org/sdd/na/table18.xlsx"
    url = 'https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1_EXPENDITURE,/A.AUS.......XDC.V..?startPeriod=2019&dimensionAtObservation=AllDimensions'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Read the content of the response
        content = response.content.decode('utf-8')

        # Load the content into a DataFrame
        df = pd.read_csv(StringIO(content))

        # Display the first few rows of the DataFrame
        print(df.head())

        return (df)
    else:
        print(f"Failed to retrieve data: {response.status_code}")


def get_from_oecd(sdmx_query):
    return pd.read_csv(
        f"https://stats.oecd.org/SDMX-JSON/data/{sdmx_query}?contentType=csv"
    )


def get_yahoo_stock(symbols: list = ['IBM', 'MSFT', 'INTC', 'META', 'NEM', 'AU', 'AEM', 'GFI']):
    import yfinance as yf

    symbols = symbols
    data = yf.download(symbols)
    portofolio_returns = data['Adj Close'].pct_change().dropna()


def get_index_data():
    import pandas_datareader.data as web
    f = web.DataReader('^DJI', 'stooq')


def get_world_bank():
    import wbgapi as web

    web.search('GDp')


def imf_data():
    import requests  # Python 3.6

    url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'

    # url = 'http://dataservices.imf.org/REST/SDMX_XML.svc/'

    # International Financial Statistics("IFS"),
    # Balance
    # of
    # Payments("BOP"), etc.

    # Navigate to series in API-returned JSON data

    key = 'CompactData/IFS/M.GB.PMP_IX'  # adjust codes here
    ij = requests.get('https://www.imf.org/external/datamapper/api/v1/NGDP_RPCH')
    o = requests.get('https://www.imf.org/external/datamapper/api/v1')
    # key = 'CompactData/IFS/M.GB.TBG_USD'
    data = (requests.get(f'{url}{key}').json()['CompactData']['DataSet']['Series'])

    key = 'Dataflow'  # Method with series information
    search_term = 'Global Debt'  # 'Trade'  # Term to find in series names
    series_list = requests.get(f'{url}{key}').json()['Structure']['Dataflows']['Dataflow']
    # Use dict keys to navigate through results:
    for series in series_list:
        if search_term in series['Name']['#text']:
            print(f"{series['Name']['#text']}: {series['KeyFamilyRef']['KeyFamilyID']}")

    key = 'DataStructure/DOT'  # Method / series
    dimension_list = requests.get(f'{url}{key}').json() \
        ['Structure']['KeyFamilies']['KeyFamily'] \
        ['Components']['Dimension']
    codelist = '@codelist'
    for n, dimension in enumerate(dimension_list):
        print(f'Dimension {n + 1}: {dimension[codelist]}')

    key = f"CodeList/{dimension_list[2]['@codelist']}"
    code_list = requests.get(f'{url}{key}').json() \
        ['Structure']['CodeLists']['CodeList']['Code']
    for code in code_list:
        print(f"{code['Description']['#text']}: {code['@value']}")


def omega_imf():
    import requests
    import pandas as pd
    import enum

    # Define the API URL
    url = 'https://www.imf.org/external/datamapper/api/v1/indicators'

    # Send a GET request to the API URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the data options (Assuming they are in the 'data' key)
        data_options = data['indicators'].keys()

        # Create an enum class dynamically
        DataOptionsEnum = enum.Enum('DataOptionsEnum', {option: option for option in data_options})

        # Print the enum class members
        for option in DataOptionsEnum:
            print(option)
    else:
        print(f"Failed to retrieve data: {response.status_code}")


class IMFClient:
    """
    A client for interacting with the IMF's API
    Documentation: http://datahelp.imf.org/knowledgebase/articles/667681
    """

    def __init__(self):
        self.base_url = "http://dataservices.imf.org/REST/SDMX_JSON.svc"

    def get_databases(self) -> List[Dict]:
        """Get list of all available IMF databases"""
        url = f"{self.base_url}/Dataflow"
        response = requests.get(url)
        return response.json()['Structure']['Dataflows']['Dataflow']

    def get_dimensions(self, database_id: str) -> Dict:
        """Get dimensions for a specific database"""
        url = f"{self.base_url}/DataStructure/{database_id}"
        response = requests.get(url)
        return response.json()['Structure']['DimensionList']['Dimension']

    def get_data(
            self,
            database_id: str,
            series_code: str,
            country_codes: Union[str, List[str]],
            start_year: Optional[int] = None,
            end_year: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Fetch data from IMF database

        Args:
            database_id: ID of the database (e.g., 'IFS' for International Financial Statistics)
            series_code: Code for the specific data series
            country_codes: Single country code or list of codes
            start_year: Starting year for data (optional)
            end_year: Ending year for data (optional)

        Returns:
            DataFrame with the requested data
        """
        # Format country codes
        if isinstance(country_codes, list):
            country_codes = '+'.join(country_codes)

        # Build URL
        url = f"{self.base_url}/CompactData/{database_id}"
        url += f"/{country_codes}.{series_code}"

        # Add time parameters if specified
        if start_year and end_year:
            url += f"?startPeriod={start_year}&endPeriod={end_year}"

        # Make request
        response = requests.get(url)
        data = response.json()

        # Extract and format data
        try:
            series = data['CompactData']['DataSet']['Series']
            if not isinstance(series, list):
                series = [series]

            # Create DataFrame
            records = []
            for s in series:
                country = s['@REF_AREA']
                observations = s['Obs']
                if not isinstance(observations, list):
                    observations = [observations]

                for obs in observations:
                    records.append({
                        'country': country,
                        'year': obs['@TIME_PERIOD'],
                        'value': obs['@OBS_VALUE']
                    })

            return pd.DataFrame(records)

        except KeyError:
            print("Error parsing data. Raw response:")
            print(data)
            return pd.DataFrame()


if __name__ == '__main__':
    # Create client instance
    imf = IMFClient()

    # List available databases
    databases = imf.get_databases()

    # Get dimensions for a specific database (e.g., IFS)
    dimensions = imf.get_dimensions('IFS')

    # Fetch GDP data for the US and UK from 2010-2020
    data = imf.get_data(
        database_id='IFS',
        series_code='NGDP_XDC',  # Nominal GDP in local currency
        country_codes=['US', 'GB'],
        start_year=2010,
        end_year=2020
    )

    print('hello')
    # omega_imf()
