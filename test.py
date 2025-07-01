import json
import uuid
import time

DB_PATH = "database.json"


def add_timer_to_db():
    # Reads data
    with open(DB_PATH, "r") as f:
        data = json.load(f)

    # Updates data with new user
    data[f"{uuid.uuid4()}"] = {
        # "start_time": a
        # "end_time": a
        # "subscribers": [user]
    }
    print(data)

    # Overwrite the json file with new data
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)


def notify():
    # Check db entries
    with open(DB_PATH, "r") as f:
        data = json.load(f)
    
    for key in data:
        entry = data[key]

        elapsed_time = time.time() - entry["start_time"]
        total_time = entry["end_time"] - entry["start_time"]

        # Half way mark
        if elapsed_time > total_time / 2:
            # Notify subscribers
            subscribers = entry["subscribers"]
            for user in subscribers:
                print(user)
                # channel = user.dm_channel
                # await channel.send()

notify()