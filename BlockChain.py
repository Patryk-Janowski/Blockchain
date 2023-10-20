from Block import Block
from CryptOperations import CryptOperations
from NetworkOperations import NetworkOperations
from concurrent.futures import ThreadPoolExecutor
import json


class Blockchain(CryptOperations, NetworkOperations):
    def __init__(self, blockchain_address):
        super().__init__()
        print(self.__dict__)
        self.chain = list()
        self.my_ip = self.get_my_ip()
        self.users = {self.my_key: self.my_ip}

    def create_and_send_block(self, data):
        new_block = Block(owner_key=self.my_key,
                          data=data,
                          index=len(self.chain),
                          previous_hash=self.chain[-1]["BlockHash"] if self.chain else "0")
        new_block_hash = new_block.mine_block()
        self.append_block(new_block, new_block_hash)
        self.send_blockchain()

    def append_block(self, block: Block, block_hash: str):
        self.chain.append({"Block": block, "BlockHash": block_hash})

    def validate_blockchain(self, blockchain: list({"Block": Block, "BlockHash": str})):
        for i, b in enumerate(blockchain):
            if not b["Block"].validate_block() and \
                (blockchain[i]["BlockHash"] == b["Block"].hash and
                 blockchain[i]["Block"].previous_hash == blockchain[i-1]["BlockHash"]):
                return False
        return True

    @property
    def block_owners(self):
        return set(x["Block"].owner_key for x in self.chain)

    @property
    def users_ips(self):
        return set(self.users.values())

    def get_block(self, index) -> Block:
        return self.chain[index]["Block"]

    def get_hash(self, index):
        return self.chain[index]["BlockHash"]

    def get_block_with_hash(self, block_hash) -> Block:
        return list(filter(lambda x: x["BlockHash"] == block_hash, self.chain))[0]["Block"]

    def send_blockchain(self):
        chain_bytes = self.serialize_chain().encode('utf-8')
        with ThreadPoolExecutor() as executor:
            executor.map(lambda ip: self.send_data_util(
                ip, self.block_port, chain_bytes), self.users_ips)

    def listen_for_blocks(self):
        tmp_chain = self.deserialize_chain(self.receive_data_util(NetworkOperations.block_port))
        if len(tmp_chain) > len(self.chain) and self.validate_blockchain(tmp_chain):
            self.chain = tmp_chain
            print("Recieved_block")
        else:
            return

    def send_user_info(self):
        # self.users
        pass

    def listen_for_users(self):
        received_users = set()
        self.users.update(received_users)
        self.send_user_info()
        self.send_blockchain()

    def serialize_chain(self):
        return json.dumps(self.chain, default=Block.serialize_block)

    def deserialize_block(self, block_json):
        return {"Block": Block(
            owner_key=block_json['Block']['owner_key'],
            index=block_json['Block']['index'],
            previous_hash=block_json['Block']['previous_hash'],
            data=block_json['Block']['data'],
            nonce=block_json['Block']['nonce']),
            "BlockHash": block_json["BlockHash"]}

    def deserialize_chain(self, json_chain_str: str):
        json_chain = json.loads(json_chain_str)
        return list(map(self.deserialize_block, json_chain))

    def mineeeeeee(self):
        block_interrupt = 0
        block_num = 0
        while True:
            self.create_block(f"{self.my_id}-{block_num}")
            if block_interrupt:
                continue

    def join_blockchain(self, blockchain_address):
        self.send_user_info()
        self.listen_for_users()
        self.listen_for_blocks()
        self.mineeeeeee()
