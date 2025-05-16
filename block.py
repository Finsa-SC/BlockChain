import hashlib
import json
import time


class Block:
    def __init__(self, index, timestamp, sender, recipient, amount, previous_hash=''):
        self.index = index
        self.timestamp = timestamp
        self.sender = self.hash_user(sender)
        self.recipient = self.hash_user(recipient)
        self.amount = amount
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_data).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"🧱 Block #{self.index} mined: {self.hash}")

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }

    @staticmethod
    def hash_user(username: str) -> str:
        return hashlib.sha256(username.encode()).hexdigest()
