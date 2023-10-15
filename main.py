from hashlib import sha256
import json, secrets, base64, os, struct, socket
from jsonpath import JSONPath
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature



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

    def get_block(self):
        return self.__dict__
    
    
class Blockchain():
    def __init__(self, blockchain_address):
        self.my_id = self.generate_secure_id()
        # self.users_ips = self.join_blockchain(blockchain_address)
        self.chain = list()
        self.my_ip = self.get_my_ip()
        self.pub_key, self.__priv_key = self.generate_keys(self.my_id)
        self.users= dict()
        self.owners_ip = dict()


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


    def generate_keys(self, prefix):
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        # Generate public key
        public_key = private_key.public_key()
        # Save private key
        with open(f"{prefix}_private_key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            ))

        # Save public key
        with open(f"{prefix}_public_key.pem", "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ))

        return public_key, private_key
    

    def sign_message(self, message):
        signature = self.__priv_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature
    

    def verify_signature(self, public_key_pem, message, signature):
        public_key = serialization.load_pem_public_key(public_key_pem)
        try:
            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False
        


    def generate_secure_id(self, length=32):
        # Generate random bytes
        random_bytes = secrets.token_bytes(length)
        
        # Encode the bytes in URL-safe base64 format
        secure_id = base64.urlsafe_b64encode(random_bytes).rstrip(b'=')
        
        return secure_id.decode('utf-8')




    @property
    def block_owners(self):
        return set(x["Block"].owner_key for x in self.chain)
    
    def create_blockchain(self, data):
        #create initial block
        new_block = Block(owner_key=self.pub_key, 
                          data=data, 
                          index=len(self.chain),
                          previous_hash="0")
        new_block_hash = new_block.mine_block()
        self.chain.append({"Block": new_block, "BlockHash": new_block_hash})
        self.owners_ip[self.pub_key.public_numbers()] = self.my_ip 
        
    def create_block(self, data):
        new_block = Block(owner_key=self.pub_key, 
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

    
    def get_block_with_hash(self, block_hash) -> Block:
        return list(filter(lambda x: x["BlockHash"]==block_hash, self.chain))[0]["Block"]
 
    
bc = Blockchain(1)
bc.create_blockchain("xd")
bc.create_block("hehehe")
print(bc.chain[0]["Block"])
print(bc.chain[1]["Block"])
hash_of_second_block = bc.chain[1]["BlockHash"]
print(bc.get_block_with_hash(hash_of_second_block).previous_hash)
print(bc.validate_blockchain(bc.chain))
print(bc.owners_ip)