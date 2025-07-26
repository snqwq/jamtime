import json
import uuid
import pathlib

queue = {}  # use later if race conditions become an issue


def initialize_db(path: str) -> None:
    """Sets up the database by creating the JSON file if it doesn't exist.

    Args:
        path (str): Path to database file
    """
    if not pathlib.Path(path).exists():
        with open(path, "w") as f:
            json.dump({}, f)


def get_db_data(path: str) -> dict:
    """Returns data from the specified JSON file.

    Args:
        path (str): Path to database file

    Returns:
        dict: Data from database
    """
    with open(path, "r") as f:
        data = json.load(f)
    return data


def write_db_data(path: str, new_data: dict, indentation: int = 4) -> None:
    """Writes `new_data` into the JSON file at `path`

    Args:
        path (str): Path to database file
        new_data (dict): Data to be written to the database
        indentation (int, optional): Indentation in the JSON file. Defaults to 4.
    """
    with open(path, "w") as f:
        json.dump(new_data, f, indent=indentation)


def get_user_subscriptions(path: str, user_id: int) -> list:
    """Gets a list of subscriptions for a user

    Args:
        path (str): Path to database file
        user_id (int): User ID to get the subscriptions of.

    Returns:
        list: List of user subscriptions
    """
    user_subscriptions = []

    data = get_db_data(path)
    for key in data:
        entry = data[key]
        for subscriber in entry["subscribers"]:
            if subscriber == user_id:
                user_subscriptions.append(f"{entry['name']} ({key})")
                break

    return user_subscriptions


def short_id_to_key(path: str, short_id: str) -> str:
    """Gets the key associated with a short ID.

    Args:
        path (str): Path to the database file.
        short_id (str): Short ID to look up.

    Returns:
        str: Key associated with the short ID, or None if not found.
    """
    data = get_db_data(path)
    for key in data:
        entry = data[key]
        if entry["short_id"] == short_id.upper():
            if entry["active"]:
                return key
    # check if the short_id is actually a key already
    if short_id in data:
        return short_id

    return None

