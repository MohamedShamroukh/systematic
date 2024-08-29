from scholarly import scholarly, ProxyGenerator
import csv
import time

# Configure a proxy generator
pg = ProxyGenerator()
if pg.FreeProxies():
    scholarly.use_proxy(pg)
    print("Using free proxies.")
else:
    print("Failed to set up proxy. Continuing without proxy.")
    scholarly.use_proxy(None)

# Define the search query
search_query = (
    '("people movements" OR "spatial movements" OR "pedestrian movement" OR "pedestrian trajectory" '
 OR "pedestrian flow" OR "pedestrian traffic" OR "pedestrian simulation", 
    'OR "pedestrian modeling" OR "pedestrian crowds") AND (GPS OR Bluetooth OR CCTV OR Wifi OR survey) '
    'AND NOT ("Vehicle" AND "autonomous" AND "car")'
)

# Function to filter results by year
def is_within_year_range(year, start_year=2020, end_year=2024):
    try:
        year = int(year)
        return start_year <= year <= end_year
    except ValueError:
        return False

# Function to perform the search with retry logic
def perform_search(query, retries=5, delay=60):
    for attempt in range(retries):
        try:
            search_results = scholarly.search_pubs(query)
            return search_results
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    raise Exception("Max retries exceeded. Cannot fetch from Google Scholar.")

# Perform the search
search_results = perform_search(search_query)

# Open a CSV file to save the results
with open('citations.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Authors", "Year", "Venue", "Citations"])

    # Process each search result
    for i, result in enumerate(search_results):
        try:
            # Extract publication year and filter by the desired range
            publication_year = result['bib'].get('pub_year', 'N/A')
            if not is_within_year_range(publication_year):
                continue

            # Extract other required fields
            title = result['bib']['title']
            authors = ", ".join(result['bib']['author'])
            venue = result['bib'].get('venue', 'N/A')
            citations = result.get('num_citations', 0)

            # Write the result to the CSV file
            writer.writerow([title, authors, publication_year, venue, citations])

            # Print progress every 100 records processed
            if (i + 1) % 100 == 0:
                print(f'{i + 1} records processed.')

            # Sleep to avoid rate limiting
            time.sleep(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

    print('Export completed.')
