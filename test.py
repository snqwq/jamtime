import json
import uuid

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
    # check db entries
    with open(DB_PATH, "r") as f:
        data = json.load(f)
    
    print(data)
    
    for key in data:
        entry = data[key]
        subscribers = entry["subscribers"]
        print(subscribers)
        #entry

        # half way mark
        # if (time.time() - entry.start_time) > (entry.end_time - entry.start_time) / 2:
        #     user = entry.subscriber

    # channel = user.dm_channel
    # await channel.send()
    

    # # checks if user is in data
    # if user_id not in data['users']:
    #     # checks if data is type list
    #     if type(data) is dict:
    #         data = [data]
    #         print(type(data))



notify()