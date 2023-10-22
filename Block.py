from hashlib import sha256
from CryptOperations import CryptOperations
import asyncio


class Block:
    first_ones = 5

    def __init__(self, index, previous_hash, data, owner_key, nonce=0):
        self.owner_key = owner_key
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = nonce

    @classmethod
    def set_interrupt_event(cls, event):
        cls.interrupt_event = event

    @property
    def hash(self) -> int:
        return sha256(str(self.__dict__).encode()).hexdigest()

    @property
    def public_key(self):
        return CryptOperations.deserialize_rsa_public_key(self.owner_key)

    def mine_block(self):
        self.nonce = 0
        while not self.hash.startswith('1' * Block.first_ones) and not Block.interrupt_event.is_set():
            if self.nonce % 10000 == 0:
                print(f"sleeping after {self.nonce} checks")
                asyncio.sleep(0.1)
            self.nonce += 1
        print(f'Mined block {self.__dict__}')
        return self.hash

    def validate_block(self):
        return self.hash.startswith('1' * Block.first_ones)

    def __str__(self):
        return f"""Owner: {self.owner_key}
Index: {self.index}
Previous hash: {self.previous_hash}
Data: {self.data}
Nonce: {self.nonce}
Hash: {self.hash}"""

    def serialize_block(self):
        # new_dict = self.__dict__.copy()
        # new_dict.pop("c", None)
        return self.__dict__

    def deserialize_block(self, block_json):
        return {"Block": Block(
            owner_key=block_json['Block']['owner_key'],
            index=block_json['Block']['index'],
            previous_hash=block_json['Block']['previous_hash'],
            data=block_json['Block']['data'],
            nonce=block_json['Block']['nonce']),
            "BlockHash": block_json["BlockHash"]}
