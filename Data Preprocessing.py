import pandas as pd
import numpy as np

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('data.csv')

# Step 1: Handle missing values in the "channel_Info" and "Category" columns
# Remove rows with missing values
df = df.dropna(subset=['channel_Info', 'Category'])

# Step 2: Standardize the formatting of the "Followers" and "Avg. Likes" columns
# Convert the "Followers" column to string data type
df['Followers'] = df['Followers'].astype(str)

# Remove the "M" suffix and convert the values to numeric
df['Followers'] = df['Followers'].str.replace('M', '').astype(float) * 1000000

# Remove the "K" suffix and convert the values to numeric
df['Followers'] = df['Followers'].astype(str).str.replace('K', '').astype(float) * 1000

# Convert the "Avg. Likes" column to string data type
df['Avg. Likes'] = df['Avg. Likes'].astype(str)

# Remove the "K" suffix and convert the values to numeric
df['Avg. Likes'] = df['Avg. Likes'].str.replace('K', '').astype(float) * 1000

# Step 3: Perform data validation and cleaning
# Check for duplicates and remove them
df.drop_duplicates(inplace=True)

# Validate and clean other columns as needed
# Ensure the "Eng Rate" column is in the correct format (percentage)
df['Eng Rate'] = df['Eng Rate'].str.rstrip('%').astype(float) / 100

# Convert "rank" column to integer
df['rank'] = df['rank'].astype(int)

# Convert "Posts" column to integer
df['Posts'] = df['Posts'].str.replace('K', '').astype(float) * 1000
df['Posts'] = df['Posts'].astype(int)

# Step 4: Handle categorical variables
# Perform one-hot encoding for the "Category" column
df = pd.get_dummies(df, columns=['Category'], prefix='Category')

# Step 5: Rename columns to remove spaces and dots
df.columns = [col.replace(' ', '_').replace('.', '_') for col in df.columns]

# Save the updated DataFrame to a new CSV file
df.to_csv('preprocessed_data.csv', index=False)

# Print the updated DataFrame
print(df.head())
print(df.info())
