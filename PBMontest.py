import requests

API_KEY = open('SearchKey.txt').read().strip()
SEARCH_ENGINE_ID = open('SearchEngineKey').read().strip()

# Open the file for reading
with open("dorklist.txt", "r") as query_list:
    # Read all lines into a list
    queries = query_list.readlines()

# Open the results file for appending
with open("results.txt", "a") as results_file:
    # Iterate through the list of queries
    for query in queries:
        # Remove leading/trailing whitespaces and newline characters
        query = query.strip()

        url = 'https://www.googleapis.com/customsearch/v1'

        params = {
            'q': query,
            'key': API_KEY,
            'cx': SEARCH_ENGINE_ID
        }

        response = requests.get(url, params=params)

        try:
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()  # Parse JSON response

            # Check if response contains items
            if 'items' in data:
                results = data['items']
                for item in results:
                    title = item.get('title', 'No title available')
                    link = item.get('link', 'No link available')
                    description = item.get('snippet', 'No description available')
                    results_file.write(f"Query: {query}\n")
                    results_file.write(f"Title: {title}\n")
                    results_file.write(f"Link: {link}\n")
                    results_file.write(f"Description: {description}\n\n")
            else:
                results_file.write(f"No search results found for query: {query}\n")
        except requests.exceptions.HTTPError as http_err:
            results_file.write(f"HTTP error occurred for query: {query} - {http_err}\n")
        except requests.exceptions.JSONDecodeError as json_err:
            results_file.write(f"JSON decoding error occurred for query: {query} - {json_err}\n")
