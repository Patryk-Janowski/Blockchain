from hashlib import sha256
import json
import os, struct

class Block:
    def __init__(self, index, previous_hash, data, owner_id, nonce=0):
        self.owner = owner_id
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = nonce

    @property
    def hash(self) -> int:
        return sha256(str(self.__dict__).encode()).hexdigest()

    def mine_block(self):
        self.nonce = 0
        while not self.hash.startswith('1' * 4):
            self.nonce += 1
        return self.hash
    
    def __str__(self):
        return f"""Owner: {self.owner}\
Index: {self.index}
Previous hash: {self.previous_hash}
Data: {self.data}
Nonce: {self.nonce}
Hash: {self.hash}"""

    def get_block(self):
        return self.__dict__
    
    
class Blockchain():
    def __init__(self, blockchain_address):
        # self.users_ips = self.join_blockchain(blockchain_address)
        self.chain = list()
        self.my_id = struct.unpack('I', os.urandom(4))[0]

    def join_blockchain(self, blockchain_address):
        # return {"Chain": chain, "UserIps": set(users_ips)}
        pass

    def publish_block(self, block: Block, block_hash):
        return True

    def listen_for_blocks(self):
        pass

    @property
    def block_owners(self):
        return set(x["Block"].owner_id for x in self.chain)
    
    def create_blockchain(self, data):
        new_block = Block(owner_id=self.my_id, 
                          data=data, 
                          index=len(self.chain),
                          previous_hash="0")
        new_block_hash = new_block.mine_block()
        self.chain.append({"Block": new_block, "BlockHash": new_block_hash})
        
    def add_block(self, data):
        new_block = Block(owner_id=self.my_id, 
                          data=data, 
                          index=len(self.chain),
                          previous_hash=self.chain[-1]["BlockHash"])
        new_block_hash = new_block.mine_block()
        if self.publish_block(new_block, new_block_hash):
            self.chain.append({"Block": new_block, "BlockHash": new_block_hash})


            
    
bc = Blockchain(1)
bc.create_blockchain("xd")
bc.add_block("hehehe")
print(bc.chain[0]["Block"])
print(bc.chain[1]["Block"])