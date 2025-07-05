from services import userdata
import random
import string
import uuid
import time

DB_PATH = "database.json"


def generate_dummy_data(
    num_entries: int, userid: int, min_duration: int, max_duration: int
) -> dict:
    data = {}
    for i in range(num_entries):
        name = f"Timer {i}"
        short_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        start_time = time.time()
        end_time = start_time + 60 * random.randint(min_duration, max_duration)
        subscribers = [userid]

        data[str(uuid.uuid4())] = {
            "name": name,
            "short_id": short_id,
            "active": True,
            "halfway": False,
            "start_time": start_time,
            "end_time": end_time,
            "subscribers": subscribers,
        }

    userdata.write_db_data(DB_PATH, data)


generate_dummy_data(100, 686709101044039769, 2, 60)
