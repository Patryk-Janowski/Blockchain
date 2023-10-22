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

    async def mine_block(self):
        self.nonce = 0
        while not self.hash.startswith('1' * Block.first_ones) and not Block.interrupt_event.is_set():
            if self.nonce % 10000 == 0:
                asyncio.sleep(0.1)
            self.nonce += 1
        if Block.interrupt_event.is_set():
            print(f'Mining was interrupted')
            return False
        else:
            print(f'Mined block {self.__dict__}')
            return self.hash

    def validate_block(self):
        return self.hash.startswith('1' * Block.first_ones) and \
            self.previous_hash is not None and \
            self.previous_hash != "None"
            # CryptOperations.is_valid_sha256(self.previous_hash)

    def __str__(self):
        return f"""Owner: {self.owner_key}
Index: {self.index}
Previous hash: {self.previous_hash}
Data: {self.data}
Nonce: {self.nonce}
Hash: {self.hash}"""

    def serialize_block(self):
        return self.__dict__

    def deserialize_block(self, block_json):
        return {"Block": Block(
            owner_key=(int(block_json['Block']['owner_key'][0]),
                       int(block_json['Block']['owner_key'][1])),
            index=block_json['Block']['index'],
            previous_hash=block_json['Block']['previous_hash'],
            data=block_json['Block']['data'],
            nonce=block_json['Block']['nonce']),
            "BlockHash": block_json["BlockHash"]}
