import plyvel
import json

db = plyvel.DB('./db/blockchain', create_if_missing=True)

def save_block(index, block_data: dict):
    db.put(str(index).encode(), json.dumps(block_data).encode())

def load_block(index):
    data = db.get(str(index).encode())
    return json.loads(data.decode()) if data else None

def load_all_blocks():
    blocks = []
    for key, value in db:
        blocks.append(json.loads(value.decode()))
    return blocks

def get_latest_index():
    last_index = -1
    for key, _ in db:
        last_index = max(last_index, int(key.decode()))
    return last_index
