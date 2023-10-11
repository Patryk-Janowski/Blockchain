from hashlib import sha256
import json
import os, struct
import socket
import JSONpath


class Block:
    def __init__(self, index, previous_hash, data, owner, nonce=0):
        self.owner = owner
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
        return f"""Owner: {self.owner}
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
        self.my_ip = self.get_my_ip()
        self.owners_ip = dict()

    def join_blockchain(self, blockchain_address):
        self.send_ips()
        self.listen_for_ips()
        self.listen_for_blocks()
        pass

    def publish_block(self, block: Block, block_hash):
        #port 50000
        tmp_blockchain = self.chain.copy()
        tmp_blockchain.append({"Block": block, "BlockHash": block_hash})
        # send tmp block
        # wait for blocks
        if True:
            self.chain = tmp_blockchain
        return True
    
    def send_blockchain(self):
        pass

    def listen_for_blocks(self):
        #port 50000
        pass

    def wait_for_votes(self):
        #port 50001
        pass

    def vote_for_block(self):
        #port 50001
        pass

    def send_ips(self):
        #port 50002
        pass

    def listen_for_ips(self):
        #port 50002
        self.send_blockchain()
        pass

    def get_my_ip(self):
        try:
            # get the host name
            host_name = socket.gethostname()
            # get the IP address
            host_ip = socket.gethostbyname(host_name)
            return host_ip
        except socket.error as err:
            print(f"Unable to get Hostname and IP. Error: {str(err)}")


    @property
    def block_owners(self):
        return set(x["Block"].owner for x in self.chain)
    
    def create_blockchain(self, data):
        #create initial block
        new_block = Block(owner=self.my_id, 
                          data=data, 
                          index=len(self.chain),
                          previous_hash="0")
        new_block_hash = new_block.mine_block()
        self.chain.append({"Block": new_block, "BlockHash": new_block_hash})
        self.owners_ip[self.my_id] = self.my_ip 
        
    def create_block(self, data):
        new_block = Block(owner=self.my_id, 
                          data=data, 
                          index=len(self.chain),
                          previous_hash=self.chain[-1]["BlockHash"])
        new_block_hash = new_block.mine_block()
        self.publish_block(new_block, new_block_hash)
        
            
    def validate_blockchain(self, block: Block, block_hash):
        return block.hash == block_hash and self.chain
 
    
bc = Blockchain(1)
bc.create_blockchain("xd")
bc.create_block("hehehe")
print(bc.chain[0]["Block"])
print(bc.chain[1]["Block"])
print(bc.block_owners)
print(bc.owners_ip)