import pandas as pd

# File paths
first_file = "./modified_AF_rows_with_variants.csv"  # Replace with your first file name
second_file = "./combined_energies_differences.csv"  # Replace with your second file name
output_file = "./TestPathogenic.csv"  # Output file name

# Load the two CSV files
df1 = pd.read_csv(first_file)  # First file with Pdb column
df2 = pd.read_csv(second_file)  # Second file with Mutation column

# Extract base names for matching
df1['Base_Name'] = df1['Pdb'].str.replace(r"(_\d+\.pdb)$", "", regex=True)
df2['Base_Name'] = df2['Mutation'].str.replace(r"(\.txt)$", "", regex=True)

# Merge based on Base_Name
merged_df = pd.merge(df1, df2, on='Base_Name', how='left')

# Drop the temporary 'Base_Name' column
merged_df = merged_df.drop(columns=['Base_Name'])

# Save the merged DataFrame to a new CSV file
merged_df.to_csv(output_file, index=False)

print(f"Merged output saved to {output_file}")
