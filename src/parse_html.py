from bs4 import BeautifulSoup
import json

def html_to_json(html_content):
    """
    Converts HTML content (with the structure from paste.txt) to JSON.

    Args:
        html_content (str): The HTML content to parse.

    Returns:
        str: JSON string representation of the parsed data.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    data = {"TRENDConnect": {"Regular Releases": {"25.04": {"tests": []}}}}

    table = soup.find('table', {'class': 'scriptGrid'})
    if table:
        rows = table.find_all('tr', class_=['parent', 'leaf'])
        current_parent = None
        for row in rows:
            if 'parent' in row['class'] and 'leaf' not in row['class']:
                # Start of a parent test case
                test_id = row.find('td', class_='id').text.strip()
                test_case = row.find('td', class_='case').text.strip()
                current_parent = {
                    "id": test_id,
                    "case": test_case,
                    "result": None,
                    "sub_tests": []
                }
                data["TRENDConnect"]["Regular Releases"]["25.04"]["tests"].append(current_parent)
            elif 'leaf' in row['class']:
                # Sub-test case
                test_id = row.find('td', class_='id').text.strip()
                test_case = row.find('td', class_='case').text.strip()
                result_td = row.find('td', class_='result')
                result = "pass" if result_td and 'pass' in result_td.get('class', []) else "fail" if result_td and 'fail' in result_td.get('class', []) else None

                sub_test = {
                    "id": test_id,
                    "case": test_case,
                    "result": result
                }
                if current_parent is not None:
                    current_parent["sub_tests"].append(sub_test)

    return json.dumps(data, indent=2)