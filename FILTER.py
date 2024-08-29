import pandas as pd


def filter_records(df):
    # Define keywords and exclude terms for filtering
    keywords = [
        "people movements", "spatial movements", "pedestrian movement",
        "pedestrian trajectory", "walking in small towns", "pedestrian flow",
        "pedestrian traffic", "pedestrian simulation", "pedestrian modeling",
        "pedestrian crowds"
    ]
    exclude_terms = ["vehicle", "autonomous", "car"]

    # Function to filter titles and abstracts
    def record_filter(title, abstract):
        title_lower = title.lower() if isinstance(title, str) else ""
        abstract_lower = abstract.lower() if isinstance(abstract, str) else ""

        contains_keywords_title = any(keyword in title_lower for keyword in keywords)
        contains_keywords_abstract = any(keyword in abstract_lower for keyword in keywords)
        contains_exclude_terms = any(term in title_lower or term in abstract_lower for term in exclude_terms)

        return (contains_keywords_title or contains_keywords_abstract) and not contains_exclude_terms

    # Apply record filtering
    filtered_df = df[df.apply(lambda row: record_filter(row['Title'], row['Abstract']), axis=1)]

    return filtered_df


def process_file(input_file, output_file):
    # Read CSV into DataFrame
    df = pd.read_csv(input_file)

    # Track number of records before filtering
    num_records_before_filtering = len(df)

    # Filter records based on title and abstract
    filtered_df = filter_records(df)

    # Track number of records after initial filtering
    num_records_after_filtering = len(filtered_df)

    # Deduplicate based on 'title' column
    final_df = filtered_df.drop_duplicates(subset='Title')

    # Track number of records after deduplication
    num_records_after_deduplication = len(final_df)

    # Calculate removed and matched records
    records_removed = num_records_before_filtering - num_records_after_deduplication
    records_matched = num_records_after_deduplication

    # Save final DataFrame to CSV
    final_df.to_csv(output_file, index=False)

    # Print summary
    print(f"Records removed: {records_removed}")
    print(f"Records matched: {records_matched}")


# Define input and output files
input_file = 'combined.csv'
output_file = 'filtered_output.csv'

# Execute the process
process_file(input_file, output_file)
