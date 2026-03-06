import pandas as pd

# Define the input and output file names
input_csv_file = 'your_input_file.csv'
output_csv_file = 'your_output_file_no_duplicates.csv'

# Read the CSV file into a pandas DataFrame
try:
    df = pd.read_csv(input_csv_file)
except FileNotFoundError:
    print(f"Error: The file '{input_csv_file}' was not found.")
    exit()

# Remove duplicate rows
# By default, drop_duplicates() considers all columns to identify duplicates
# and keeps the first occurrence.
df_cleaned = df.drop_duplicates()

# Save the cleaned DataFrame to a new CSV file
# index=False prevents pandas from writing the DataFrame index as a column in the CSV
df_cleaned.to_csv(output_csv_file, index=False)

print(f"Duplicate rows removed successfully. Cleaned data saved to '{output_csv_file}'")