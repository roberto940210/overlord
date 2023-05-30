import glob
import pandas as pd
import numpy as np

# Get all Excel files in cwd using glob
excel_files = glob.glob('*.xlsx')

# Read all Excel files into dataframes
dfs = [pd.read_excel(file, dtype={'code': str}) for file in excel_files]

# Define a function to process a single DataFrame
def process_df(df):
    # Get the unique values of the 'code' column
    unique_codes = df['code'].unique()

    # Create a new DataFrame with the unique codes as the first column
    new_df = pd.DataFrame(unique_codes, columns=['code'])

    # Get the name of the second column
    second_column_name = df.columns[1]

    # Add a second column to the new DataFrame with the sum of the corresponding values from the second column of the input DataFrame
    new_df[second_column_name] = new_df['code'].apply(lambda x: df[df['code'] == x][second_column_name].sum())

    return new_df

# Process each DataFrame individually and store the results in a list
results = [process_df(df) for df in dfs]

# Display the resulting DataFrames
newdts = [x for x in results]

# Merge all dataframes on "code" column
merged_df = newdts[0]
for df in newdts[1:]:
    merged_df = pd.merge(merged_df, df, on='code', how='outer', suffixes=('','_r'))

# Save merged dataframe to Excel file
merged_df.to_excel('!CONTROL.xlsx', index=False)
print(merged_df)
