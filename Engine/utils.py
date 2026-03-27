import json
from datetime import datetime
import os
from datetime import datetime, timezone

def now_utc():
    return datetime.now(timezone.utc).isoformat()



def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
