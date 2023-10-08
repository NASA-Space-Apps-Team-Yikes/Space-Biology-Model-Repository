import pandas as pd
import numpy as np

# Read the data
df = pd.read_csv('Mouse_data.csv')

# Remove rows with 0s
df = df.loc[(df!=0).all(axis=1)]

# Split the column names to get the mouse type, test type, and mouse ID
df.columns = df.columns.str.split('_', expand=True)

# Define a function to create a new column name based on the mouse type and test type
def create_new_column_name(col):
    return f"{col[1]}_{col[3]}"

# Apply the function to each column
df.columns = df.columns.map(create_new_column_name)

# Exclude the protein column
df_numeric = df.drop(columns=[df.columns[0]])

# Average each column by mouse type and test type
df_avg = df_numeric.groupby(by=df_numeric.columns, axis=1).mean()

# Add the protein column back to the DataFrame
df_final = pd.concat([df[df.columns[0]], df_avg], axis=1)

# Rename the columns to indicate that they are averages
df_final.columns = df_final.columns + '_AVG'

# Rename the protein column
df_final.rename(columns={df_final.columns[0]: 'Protein_ID'}, inplace=True)

# Write the processed data to a new CSV file
df_final.to_csv('processed_data.csv', index=False)