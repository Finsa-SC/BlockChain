import hashlib
import json
from time import time

class Block:
    def __init__(self, index, timestamp, sender, recipient, amount, previous_hash=''):
        self.index = index
        self.timestamp = timestamp
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Hitung SHA-256 dari data block"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        """Proses mining: cari hash dengan prefix nol sebanyak difficulty"""
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"✅ Block {self.index} mined: {self.hash}")
