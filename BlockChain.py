from Block import Block
from CryptOperations import CryptOperations
from NetworkOperations import NetworkOperations
from concurrent.futures import ThreadPoolExecutor
import asyncio
import json


class Blockchain(CryptOperations, NetworkOperations, Block):
    def __init__(self, first_user_key, first_user_ip):
        super().__init__()
        print(self.__dict__)
        self.chain = list()
        self.my_ip = self.get_my_ip()
        self.users = {self.my_key: self.my_ip, first_user_key: first_user_ip}
        self.interrupt_event = asyncio.Event()
        Block.set_interrupt_event(self.interrupt_event)
        self.send_user_info()

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
        print("sending data")
        with ThreadPoolExecutor() as executor:
            executor.map(lambda ip: self.send_data_util(
                ip, self.block_port, chain_bytes), self.users_ips)

    def send_user_info(self):
        users_bytes = self.serialize_users().encode('utf-8')
        with ThreadPoolExecutor() as executor:
            executor.map(lambda ip: self.send_data_util(
                ip, self.block_port, users_bytes), self.users_ips)

    def serialize_chain(self):
        return json.dumps(self.chain, default=Block.serialize_block)

    def serialize_users(self):
        return json.dumps(self.users)

    def deserialize_users(self, users_json_str):
        return json.loads(users_json_str)

    def deserialize_chain(self, json_chain_str: str):
        json_chain = json.loads(json_chain_str)
        return list(map(self.deserialize_block, json_chain))

    async def handle_users(self, reader, writer):
        received_users = self.deserialize_users(await self.receive_data_util(reader, writer))
        self.users.update(received_users)
        self.send_user_info()
        self.send_blockchain()

    async def handle_blocks(self, reader, writer):
        tmp_chain = self.deserialize_chain(await self.receive_data_util(reader, writer))
        if len(tmp_chain) > len(self.chain) and self.validate_blockchain(tmp_chain):
            self.chain = tmp_chain
            print("Received_block")
            self.interrupt_event.set()

    async def listen_for_users(self):
        server = await asyncio.start_server(
            self.handle_users, "0.0.0.0", self.users_port
        )
        async with server:
            await server.serve_forever()

    async def listen_for_blocks(self):
        server = await asyncio.start_server(
            self.handle_blocks, "0.0.0.0", self.block_port
        )
        async with server:
            await server.serve_forever()

    async def const_mine(self):
        block_num = 0
        while True:
            self.create_and_send_block(f"{self.my_id}-{block_num}")
            block_num += 1
            await asyncio.sleep(0.1)

    async def main(self):
        await asyncio.gather(
            self.listen_for_users(),
            self.listen_for_blocks(),
            self.const_mine()
        )
