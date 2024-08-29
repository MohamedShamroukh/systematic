# Define keywords and exclude terms for filtering
KEYWORDS = [
    "people movements", "spatial movements", "pedestrian movement",
    "pedestrian trajectory", "walking in small towns", "pedestrian flow",
    "pedestrian traffic", "pedestrian simulation", "pedestrian modeling",
    "pedestrian crowds"
]
EXCLUDE_TERMS = ["vehicle", "autonomous", "car"]

# Specify the input files and the output files
INPUT_FILES = ['scopus.csv', 'webofscience.csv', 'googlescholar.csv']
COMBINED_OUTPUT_FILE = 'combined.csv'
FINAL_OUTPUT_FILE = 'systematic-review-papers.csv'
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import subprocess
import sys
import os
# Function to install pandas if not already installed
def install_pandas():
    try:
        import pandas as pd
    except ImportError:
        print("Pandas not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
# Call the function to install pandas
install_pandas()

import pandas as pd
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

print("first stage of filtering the research papers ...............")
def combine_and_deduplicate(files, output_file):
    # Track total records before deduplication
    total_records_before = 0
    # Combine DataFrames and standardize column names
    combined_df = pd.concat([
        pd.read_csv(file).rename(columns={'Article Title': 'Title'}) for file in files
    ])

    # Display records per file
    for file in files:
        df = pd.read_csv(file)
        df.rename(columns={'Article Title': 'Title'}, inplace=True)
        print(f"Number of records in {os.path.splitext(file)[0]}: {len(df)}")
        total_records_before += len(df)

    # Remove duplicates based on 'Title' column
    combined_df.drop_duplicates(subset='Title', inplace=True)
    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv(output_file, index=False)
    # Print the number of records and duplicates removed
    print(f"Number of records in {output_file}: {len(combined_df)}")
    print(f"Duplicates removed from combined file: {total_records_before - len(combined_df)}")
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def filter_records(df):
    # Function to filter titles and abstracts
    def record_filter(title, abstract):
        title_lower = title.lower() if isinstance(title, str) else ""
        abstract_lower = abstract.lower() if isinstance(abstract, str) else ""
        contains_keywords_title = any(keyword in title_lower for keyword in KEYWORDS)
        contains_keywords_abstract = any(keyword in abstract_lower for keyword in KEYWORDS)
        contains_exclude_terms = any(term in title_lower or term in abstract_lower for term in EXCLUDE_TERMS)
        return (contains_keywords_title or contains_keywords_abstract) and not contains_exclude_terms
    # Apply record filtering
    filtered_df = df[df.apply(lambda row: record_filter(row['Title'], row['Abstract']), axis=1)]
    return filtered_df

def process_file(input_file, output_file):
    df = pd.read_csv(input_file)
    # Filter records based on title and abstract
    filtered_df = filter_records(df)
    # Deduplicate based on 'Title' column
    final_df = filtered_df.drop_duplicates(subset='Title')
    # Save final DataFrame to CSV
    final_df.to_csv(output_file, index=False)
    # Print summary
    print("2nd stage of filtering the research papers ...............")
    print(f"Records removed: {len(df) - len(final_df)}")
    print(f"Records matched: {len(final_df)}")

# Execute the process
combine_and_deduplicate(INPUT_FILES, COMBINED_OUTPUT_FILE)
process_file(COMBINED_OUTPUT_FILE, FINAL_OUTPUT_FILE)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
