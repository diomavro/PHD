import csv
import pandas as pd
import os 
from constants import directory
from functions import gather_questions_and_answers


# Create a list of column names
column_names = ["A", "B", "C"]
# Create a DataFrame with the same names for both index and columns
df = pd.DataFrame(columns=column_names, index=column_names)
# Fill the DataFrame with sample data (optional)
df.loc["A", "A"] = 1
df.loc["A", "B"] = 2
df.loc["B", "A"] = 3
df.loc["C", "C"] = 4
# Display the DataFrame
print(df)

 # Replace with the actual path to your directory
gather_questions_and_answers(A)