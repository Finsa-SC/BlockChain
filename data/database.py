import plyvel
import json

db = plyvel.DB('blockchaindb', create_if_missing=True)

def save_block(index: int, block_data: dict):
    db.put(str(index).encode(), json.dumps(block_data).encode())

def load_block(index: int):
    data = db.get(str(index).encode())
    if data:
        return json.loads(data.decode())
    return None

def load_all_blocks():
    blocks = []
    for key, value in db:
        blocks.append(json.loads(value.decode()))
    return sorted(blocks, key=lambda b: b['index'])

def get_last_index():
    keys = list(db.iterator(include_value=False))
    if not keys:
        return -1
    return int(keys[-1].decode())

def close_db():
    db.close()
