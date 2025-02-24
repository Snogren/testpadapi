import requests

def fetch_html_data(url):
    """
    Fetches HTML data from a given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content, or None if there was an error.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None