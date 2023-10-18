from hashlib import sha256
from CryptOperations import CryptOperations
import cryptography
import json

class Block:
    def __init__(self, index, previous_hash, data, owner_key, nonce=0):
        self.owner_key = owner_key
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = nonce

    @property
    def hash(self) -> int:
        return sha256(str(self.__dict__).encode()).hexdigest()
    
    @property
    def public_key(self):
        return CryptOperations.json_to_rsa_public_key(self.owner_key)

    def mine_block(self):
        self.nonce = 0
        while not self.hash.startswith('1' * 4):
            self.nonce += 1
        return self.hash
    
    def validate_block(self):
        return self.hash.startswith('1' * 4)
    
    def __str__(self):
        return f"""Owner: {self.owner_key}
Index: {self.index}
Previous hash: {self.previous_hash}
Data: {self.data}
Nonce: {self.nonce}
Hash: {self.hash}"""
    
    def serialize_block(self):
       return self.__dict__