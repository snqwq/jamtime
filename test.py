import json
import uuid

db_path = "database.json"

# reads data
with open(db_path, "r") as f:
    data = json.load(f)
    print(data)
    print(type(data))

    # # checks if user is in data
    # if user_id not in data['users']:
    #     # checks if data is type list
    #     if type(data) is dict:
    #         data = [data]
    #         print(type(data))

    # updates data with new user
    data[f"{uuid.uuid4()}"] = {"bob": "AAAAAAAAAAA"}
    print(data)

    # overwrite the json file with new data
    with open(db_path, "w") as f:
        json.dump(data, f, indent=4)
