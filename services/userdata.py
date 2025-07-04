import json
import uuid
import pathlib

queue = {}  # use later if race conditions become an issue


def get_db_data(path: str) -> dict:
    """Returns data from the specified JSON file."""
    with open(path, "r") as f:
        data = json.load(f)
    return data


def write_db_data(path: str, new_data: dict, indentation: int = 4) -> None:
    """Writes `new_data` into the JSON file at `path`"""
    with open(path, "w") as f:
        json.dump(new_data, f, indent=indentation)


def get_user_subscriptions(path: str, user_id=int) -> list:
    user_subscriptions = []

    data = get_db_data(path)
    for key in data:
        entry = data[key]
        for subscriber in entry["subscribers"]:
            if subscriber == user_id:
                user_subscriptions.append(f"{entry["name"]} ({key})")
                break

    return user_subscriptions


# def get_entry_by_shortid(path: str, )
