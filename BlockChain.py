from Block import Block
from CryptOperations import CryptOperations
from NetworkOperations import NetworkOperations
# from concurrent.futures import ThreadPoolExecutor
import asyncio
import json


class Blockchain(CryptOperations, NetworkOperations, Block):
    def __init__(self, first_user_id: str = None):
        super().__init__()
        self.chain = list()
        self.my_ip = self.get_my_ip()
        self.users = {self.my_key: self.my_ip}
        print(f"my_str_id: {self.serialize_users()}")
        if first_user_id:
            self.users.update(self.deserialize_users(first_user_id))
            print(self.users)
        self.interrupt_event = asyncio.Event()
        Block.set_interrupt_event(self.interrupt_event)

    def print_chain(self, chain):
        for b in chain:
            print(b["Block"])
            print(b["BlockHash"])
            print("*"*100)

    async def create_and_send_block(self, data):
        new_block = Block(owner_key=self.my_key,
                          data=data,
                          index=len(self.chain),
                          previous_hash=self.chain[-1]["Block"].hash if len(self.chain) > 0 else "first_block")
        new_block_hash = await new_block.mine_block()
        if new_block_hash:
            self.append_block(new_block, new_block_hash)
            await self.send_blockchain()
            await self.send_user_info()
        else:
            print("Skipping mining block")

    def append_block(self, block: Block, block_hash: str):
        self.chain.append({"Block": block, "BlockHash": block_hash})

    def validate_blockchain(self, blockchain: list({"Block": Block, "BlockHash": str})):
        if not blockchain[0]["Block"].validate_block():
            return False
        for i in range(1, len(blockchain)):
            if  blockchain[i]["Block"].validate_block() and \
                (blockchain[i]["BlockHash"] == blockchain[i]["Block"].hash and
                 blockchain[i]["Block"].previous_hash == blockchain[i-1]["BlockHash"]):
                return True
            else:
                return False

    @property
    def block_owners(self):
        return set(x["Block"].owner_key for x in self.chain)

    @property
    def users_ips(self):
        return set([x for x in self.users.values() if x != self.my_ip])

    def get_block(self, index) -> Block:
        return self.chain[index]["Block"]

    def get_hash(self, index):
        return self.chain[index]["BlockHash"]

    def get_block_with_hash(self, block_hash) -> Block:
        return list(filter(lambda x: x["BlockHash"] == block_hash, self.chain))[0]["Block"]

    async def send_blockchain(self):
        chain_bytes = self.serialize_chain().encode('utf-8')
        print("Sending chain")
        for ip in self.users_ips:
            await self.send_data_util(ip, self.block_port, chain_bytes)
        # with ThreadPoolExecutor() as executor:
        #     executor.map(lambda ip: self.send_data_util(
        #         ip, self.block_port, chain_bytes), self.users_ips)

    async def send_user_info(self):
        asyncio.sleep(1)
        users_bytes = self.serialize_users().encode('utf-8')
        for ip in self.users_ips:
            print(f"Sending user info")
            await self.send_data_util(ip, self.users_port, users_bytes)
        # with ThreadPoolExecutor() as executor:
        #     executor.map(lambda ip: self.send_data_util(
        #         ip, self.block_port, users_bytes), self.users_ips)

    def serialize_chain(self):
        return json.dumps(self.chain, default=Block.serialize_block)

    def serialize_users(self):
        return json.dumps(self.users)

    def serialize_users(self):
        serialized_users = {str(key): value for key,
                            value in self.users.items()}
        return json.dumps(serialized_users)

    def deserialize_users(self, users_json_str):
        deserialized_users = json.loads(users_json_str)
        return {(int(k.split(",")[0][1:]), int(k.split(",")[1][:-1])): v for k, v in deserialized_users.items()}

    def deserialize_chain(self, json_chain_str: str):
        json_chain = json.loads(json_chain_str)
        return list(map(self.deserialize_block, json_chain))

    async def handle_users(self, reader, writer):
        received_users = self.deserialize_users(await self.receive_data_util(reader, writer))
        self.users.update(received_users)
        print(f"BlockChain users ips: {self.users_ips}")


    async def handle_blocks(self, reader, writer):
        tmp_chain = self.deserialize_chain(await self.receive_data_util(reader, writer))
        print(f"Received chain")
        if len(tmp_chain) > len(self.chain):
            print("Received longer chain")
            print("Verifying chain\n...")
            if self.validate_blockchain(tmp_chain):
                self.chain = tmp_chain
                print("Chain was valid")
                self.interrupt_event.set()
                self.print_chain(self.chain)
            else:
                print("Chain was invalid")
        else:
            print("Chain was shorter")
        print("\n")

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
            await self.create_and_send_block(f"{self.my_id}-{block_num}")
            self.interrupt_event.clear()
            block_num += 1
            await asyncio.sleep(0.1)

    async def run_all(self):
        await asyncio.gather(
            self.send_user_info(),
            self.listen_for_users(),
            self.listen_for_blocks(),
            self.const_mine()
        )
