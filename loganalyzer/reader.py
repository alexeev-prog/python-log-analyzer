import json
from pathlib import Path


def load_log_data(filename: str):
    """Load log data by filename."""
    result_list = []

    with Path.open(filename, "r") as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line:
                try:
                    obj = json.loads(stripped_line)
                    result_list.append(obj)
                except json.JSONDecodeError as e:
                    print(f"Error when decode line: {line}. Exception: {e}")

    return result_list


def load_json_data(filename: str):
    """Load json data by filename."""
    with Path.open(filename, "r") as file:
        return json.load(file)
