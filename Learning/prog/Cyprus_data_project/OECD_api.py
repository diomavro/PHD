url = 'https://sdmx.oecd.org/public/rest/dataflow/all'

import pandas as pd

url = 'https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1_EXPENDITURE,/A........XDC.V..?dimensionAtObservation=AllDimensions'

df = pd.read_csv(url)

print('hello')

