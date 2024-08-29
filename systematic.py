import pandas as pd
import os

def combine_and_deduplicate(files, output_file):
    total_records_before = 0
    
    # Process each file
    for file in files:
        df = pd.read_csv(file)
        df.rename(columns={'Article Title': 'Title'}, inplace=True) if 'Article Title' in df.columns else None
        print(f"Number of records in {os.path.splitext(file)[0]}: {len(df)}")
        total_records_before += len(df)
    
    # Combine the DataFrames and remove duplicates based on 'Title' column
    combined_df = pd.concat([pd.read_csv(file).rename(columns={'Article Title': 'Title'}) for file in files]).drop_duplicates(subset='Title')
    
    # Save the result to a new CSV file
    combined_df.to_csv(output_file, index=False)
    
    # Print the number of records and duplicates removed
    print(f"Number of records in {output_file}: {len(combined_df)}")
    print(f"Duplicates removed from combined file: {total_records_before - len(combined_df)}")

# Specify the input files and the output file
files = ['scopus.csv', 'webofscience.csv', 'googlescholar.csv']
output_file = 'combined.csv'

# Call the function
combine_and_deduplicate(files, output_file)
