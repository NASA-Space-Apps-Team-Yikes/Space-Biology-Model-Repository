import pandas as pd
import numpy as np

# Read the data
df = pd.read_csv('Mouse_data.csv')

# Remove rows with 0s
df = df.loc[(df!=0).all(axis=1)]

# Split the column names to get the type and mouse
df.columns = df.columns.str.split('_', expand=True)

# Define a function to create a new column name based on the type, mouse, and other details
def create_new_column_name(col):
    return f"{col[0]}_{col[1]}_{col[2]}_{col[3]}_{col[4]}"

# Apply the function to each column
df.columns = df.columns.map(create_new_column_name)

# Exclude the mouse ID column
df_numeric = df.drop(columns=[df.columns[0]])

# Average each column by type and mouse
df_numeric = df_numeric.groupby(by=df_numeric.columns, axis=1).mean()

# Add the mouse ID column back to the DataFrame
df_final = pd.concat([df[df.columns[0]], df_numeric], axis=1)

# Rename the mouse ID column
df_final.rename(columns={df_final.columns[0]: 'mouse_id'}, inplace=True)

# Write the processed data to a new CSV file
df_final.to_csv('processed_data.csv', index=False)