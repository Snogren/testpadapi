import json
import os
from datetime import datetime
import Levenshtein

def calculate_diff(old_data, new_data):
    """Calculates the difference between two JSON data structures.

    Args:
        old_data (dict): The old data as a dictionary.
        new_data (dict): The new data as a dictionary.

    Returns:
        dict: A dictionary representing the changes.
    """
    diff = {}
    for key, new_value in new_data.items():
        if key in old_data:
            old_value = old_data[key]
            if isinstance(new_value, dict) and isinstance(old_value, dict):
                nested_diff = calculate_diff(old_value, new_value)
                if nested_diff:
                    diff[key] = nested_diff
            elif new_value != old_value:
                if isinstance(new_value, str) and isinstance(old_value, str):
                    distance = Levenshtein.distance(new_value, old_value)
                    diff[key] = {"old": old_value, "new": new_value, "distance": distance}
                else:
                    diff[key] = {"old": old_value, "new": new_value}
        else:
            diff[key] = {"new": new_value, "old": None}  # New key

    # Check for removed keys
    for key in old_data.keys():
        if key not in new_data:
            diff[key] = {"old": old_data[key], "new": None}

    return diff

def store_data(data, data_dir="data"):
    """Stores the JSON data to a file with a timestamp.

    Args:
        data (str): The JSON data to store.
        data_dir (str, optional): The directory to store the data files. Defaults to "data".
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(data_dir, f"data_{timestamp}.json")
    os.makedirs(data_dir, exist_ok=True)  # Ensure directory exists
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    print(f"Data stored to {filename}")
    return filename

def load_latest_data(data_dir="data"):
    """Loads the latest JSON data from the data directory.

    Args:
        data_dir (str, optional): The directory to load data from. Defaults to "data".

    Returns:
        dict: The latest data as a dictionary, or None if no data is found.
    """
    files = [f for f in os.listdir(data_dir) if f.startswith("data_") and f.endswith(".json")]
    if not files:
        return None  # No data files found

    latest_file = max(files)  # Lexicographical sort works due to timestamp format
    filepath = os.path.join(data_dir, latest_file)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {filepath}")
        return None

def generate_history(data_dir="data"):
    """Generates a history of changes from the stored JSON data files."""
    files = sorted([f for f in os.listdir(data_dir) if f.startswith("data_") and f.endswith(".json")])
    history = []
    previous_data = None

    for filename in files:
        filepath = os.path.join(data_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                current_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error processing {filename}: {e}")
            continue

        if previous_data:
            diff = calculate_diff(previous_data, current_data)
            history.append({"file": filename, "changes": diff})

        previous_data = current_data
    return history