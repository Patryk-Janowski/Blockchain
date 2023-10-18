from Block import Block
from CryptOperations import CryptOperations
from hashlib import sha256
import json, base64, os, struct, socket
from jsonpath import JSONPath
from cryptography.hazmat.primitives import serialization, hashes

class Blockchain(CryptOperations):
    def __init__(self, blockchain_address):
        self.my_id = self.generate_secure_id()
        # self.users_ips = self.join_blockchain(blockchain_address)
        self.chain = list()
        self.my_ip = self.get_my_ip()
        self.pub_key, self.__priv_key = self.generate_keys(self.my_id)
        self.my_key = self.rsa_public_key_to_json(self.pub_key)
        self.users= dict()

    def join_blockchain(self, blockchain_address):
        self.send_user_info()
        self.listen_for_users()
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

    def send_user_info(self):
        #port 50002
        pass

    def listen_for_users(self):
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
        return set(x["Block"].owner_key for x in self.chain)
    
    def get_block(self, index) -> Block:
        return self.chain[index]["Block"]
    
    def get_hash(self, index):
        return self.chain[index]["BlockHash"]
    
    def get_block_with_hash(self, block_hash) -> Block:
        return list(filter(lambda x: x["BlockHash"]==block_hash, self.chain))[0]["Block"]
    
    def create_blockchain(self, data):
        #create initial block
        new_block = Block(owner_key=self.my_key,
                          data=data, 
                          index=len(self.chain),
                          previous_hash="0")
        new_block_hash = new_block.mine_block()
        self.chain.append({"Block": new_block, "BlockHash": new_block_hash})
        self.users[self.pub_key.public_numbers()] = self.my_ip
        
    def create_block(self, data):
        new_block = Block(owner_key=self.my_key,
                          data=data, 
                          index=len(self.chain),
                          previous_hash=self.chain[-1]["BlockHash"])
        new_block_hash = new_block.mine_block()
        self.publish_block(new_block, new_block_hash)
        
    def validate_blockchain(self, blockchain: list({"Block": Block, "BlockHash": str})):
        for i, b in enumerate(blockchain):
            if not b["Block"].validate_block() and \
            (blockchain[i]["BlockHash"] == b["Block"].hash and
            blockchain[i]["Block"].previous_hash == blockchain[i-1]["BlockHash"]):
                return False
        return True
    
    def serialize_chain(self):
        return json.dumps(self.chain, default=Block.serialize_block)

    def deserialize_chain(self, json_chain_str: str):
        json_chain = json.loads(json_chain_str)
        def deserialize_util(x):
            return {"Block":Block(
                        owner_key=x['Block']['owner_key'], 
                        index=x['Block']['index'], 
                        previous_hash=x['Block']['previous_hash'], 
                        data=x['Block']['data'], 
                        nonce=x['Block']['nonce']),
                    "BlockHash": x["BlockHash"]}
        return list(map(deserialize_util, json_chain))