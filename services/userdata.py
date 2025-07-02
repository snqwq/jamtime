import json
import uuid
import pathlib

queue = {}


def get_db_data(path: str) -> dict:
    """Returns data from the specified JSON file."""
    with open(path, "r") as f:
        data = json.load(f)
    return data


def write_db_data(path: str, new_data: dict) -> None:
    with open(path, "w") as f:
        json.dump(new_data, f, indent=4)
