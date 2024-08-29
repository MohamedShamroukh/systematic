import csv

print("csv imported")
from scholarly import scholarly


def search_google_scholar(query, start_year, end_year, num_results=10):
    search_query = scholarly.search_pubs(query)
    results = []

    for i in range(num_results):
        try:
            publication = next(search_query)
            pub_year = publication['bib'].get('year', '')
            if pub_year and int(pub_year) >= start_year and int(pub_year) <= end_year:
                results.append({
                    'title': publication['bib'].get('title', ''),
                    'authors': ', '.join(publication['bib'].get('author', [])),
                    'year': pub_year,
                    'citations': publication.get('num_citations', 0),
                    'url': publication.get('pub_url', '')
                })
            elif not pub_year:
                results.append({
                    'title': publication['bib'].get('title', ''),
                    'authors': ', '.join(publication['bib'].get('author', [])),
                    'year': 'N/A',
                    'citations': publication.get('num_citations', 0),
                    'url': publication.get('pub_url', '')
                })
        except StopIteration:
            break

    return results


def save_to_csv(results, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'authors', 'year', 'citations', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)


if __name__ == "__main__":
    search_query = (
        '("people movements" OR "spatial movements" OR "pedestrian movement" OR "pedestrian trajectory" OR "pedestrian flow" OR "pedestrian traffic" OR "pedestrian simulation" '
        'OR "pedestrian modeling" OR "pedestrian crowds") AND (GPS OR Bluetooth OR CCTV OR Wifi OR survey) '
        'AND NOT ("Vehicle" AND "autonomous" AND "car")'
    )

    start_year = int(input("Enter the start year for the search: "))
    end_year = int(input("Enter the end year for the search: "))
    num_results = int(input("Enter the number of results to fetch (default 10): ") or 10)
    output_file = input("Enter the output CSV filename: ")

    results = search_google_scholar(search_query, start_year, end_year, num_results)
    save_to_csv(results, output_file)

    print(f"Search results saved to {output_file}")