import time
import plyvel
import json
from block import Block


class Blockchain:
    def __init__(self, db_path='db'):
        self.db = plyvel.DB(db_path, create_if_missing=True)
        self.difficulty = 2  # Bisa kamu ubah kalau mau lebih susah
        if not self.db.get(b'last_index'):
            print("⛓️  Genesis block not found, creating one...")
            genesis_block = Block(0, time.time(), "genesis", "genesis", 0, "0")
            genesis_block.mine_block(self.difficulty)
            self.add_block_to_db(genesis_block)

    def get_last_index(self):
        last_index_bytes = self.db.get(b'last_index')
        return int(last_index_bytes.decode()) if last_index_bytes else -1

    def get_latest_block(self):
        last_index = self.get_last_index()
        if last_index == -1:
            return None
        block_data = self.db.get(f'block_{last_index}'.encode())
        return self.deserialize_block(block_data)

    def add_block(self, sender, recipient, amount):
        last_block = self.get_latest_block()
        index = self.get_last_index() + 1
        previous_hash = last_block.hash if last_block else "0"
        new_block = Block(index, time.time(), sender, recipient, amount, previous_hash)
        new_block.mine_block(self.difficulty)
        self.add_block_to_db(new_block)

    def add_block_to_db(self, block):
        block_data = json.dumps(block.to_dict()).encode()
        self.db.put(f'block_{block.index}'.encode(), block_data)
        self.db.put(b'last_index', str(block.index).encode())
        print(f"✅ Block #{block.index} successfully added to blockchain")

    def get_all_blocks(self):
        blocks = []
        last_index = self.get_last_index()
        for i in range(last_index + 1):
            block_data = self.db.get(f'block_{i}'.encode())
            blocks.append(self.deserialize_block(block_data))
        return blocks

    def deserialize_block(self, data):
        obj = json.loads(data.decode())
        block = Block(
            obj['index'], obj['timestamp'], obj['sender'],
            obj['recipient'], obj['amount'], obj['previous_hash']
        )
        block.nonce = obj['nonce']
        block.hash = obj['hash']
        return block

    def is_valid_chain(self, chain):
        for i in range(1, len(chain)):
            current = chain[i]
            previous = chain[i - 1]

            if current['index'] != previous['index'] + 1:
                return False

            if current['previous_hash'] != previous['hash']:
                return False

            # Cek hash valid sesuai data dan nonce (kamu sesuaikan sesuai fungsi hashing kamu)
            hash_check = self.calculate_hash(
                current['index'],
                current['timestamp'],
                current['sender'],
                current['recipient'],
                current['amount'],
                current['previous_hash'],
                current['nonce']
            )
            if current['hash'] != hash_check:
                return False

        return True

    def replace_chain(self, new_chain):
        """
        Ganti chain lama dengan yang baru
        """
        # Konversi new_chain (list of dict) jadi objek block kalau perlu
        # Kalau kamu pakai dict langsung sebagai block, bisa langsung ganti
        self.chain = new_chain