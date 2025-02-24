import json
from fetch_data import fetch_html_data
from parse_html import html_to_json
from track_changes import store_data, load_latest_data, calculate_diff
from utils import handle_error

URL = "https://trendqa.testpad.com/script/65/report?auth=78a2bcc92d6063f80055393696ae527a"
DATA_DIR = "data"

def main():
    """
    Main function to fetch data, convert it to JSON, track changes, and store the history.
    """
    # 1. Fetch the data
    html_data = fetch_html_data(URL)
    if not html_data:
        handle_error("Failed to fetch data. Exiting.")
        return

    # 2. Convert to JSON
    try:
        json_data = html_to_json(html_data)
    except Exception as e:
        handle_error("Error converting HTML to JSON", e)
        return

    # 3. Load the latest data (if any)
    previous_data = load_latest_data(DATA_DIR)
    current_data = json.loads(json_data)  # Parse the JSON string to a Python dictionary

    # 4. Track changes
    if previous_data:
        diff = calculate_diff(previous_data, current_data)
        print("Changes:", json.dumps(diff, indent=2))  # Print the changes in a readable format

    # 5. Store the data
    filename = store_data(json_data, DATA_DIR)
    print(f"Data stored to {filename}")
    print("Process completed successfully.")

if __name__ == "__main__":
    main()
