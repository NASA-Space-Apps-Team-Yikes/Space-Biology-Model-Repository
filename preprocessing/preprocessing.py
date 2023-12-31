import pandas as pd
import numpy as np

# Read the data
df = pd.read_csv('Mouse_data.csv')

# Replace 0s with NaN
df.replace(0, np.nan, inplace=True)

# Split the column names to get the mouse type, test type, and mouse ID
df.columns = df.columns.str.split('_', expand=True)

# Define a function to create a new column name based on the mouse type and test type
def create_new_column_name(col):
    return f"{col[1]}_{col[3]}_{col[4]}".lower().replace('-', '_')

# Apply the function to each column
df.columns = df.columns.map(create_new_column_name)

# Exclude the protein column
df_numeric = df.drop(columns=[df.columns[0]])

# Average each column by mouse type and test type, ignoring NaN values
df_avg = df_numeric.groupby(by=df_numeric.columns, axis=1).mean()

# Add the protein column back to the DataFrame
df_final = pd.concat([df[df.columns[0]], df_avg], axis=1)

# Rename the columns to indicate that they are averages
df_final.columns = df_final.columns + '_avg'

# Rename the protein column
df_final.rename(columns={df_final.columns[0]: 'ensmbl_id'}, inplace=True)

# Split the DataFrame into two DataFrames based on the mouse type
df_c3h = df_final.filter(regex='c3h|ensmbl_id', axis=1)
df_c57 = df_final.filter(regex='c57|ensmbl_id', axis=1)

# Write each DataFrame to a different CSV file
df_c3h.to_csv('processed_data_c3h.csv', index=False)
df_c57.to_csv('processed_data_c57.csv', index=False)