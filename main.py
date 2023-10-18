import os
from BlockChain import Blockchain
from Block import Block
import json


def remove_pem_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.pem'):
            try:
                os.remove(os.path.join(directory, filename))
                print(f'Removed {filename}')
            except Exception as e:
                print(f'Error removing {filename}: {e}')

if __name__ == "__main__":
    current_directory = os.getcwd()
    remove_pem_files(current_directory)
    
    bc = Blockchain(1)
    bc.create_blockchain("xd")
    bc.create_block("hehehe")
    # print(bc.chain[1]["Block"].dump_block())

    print(json.dumps(bc.chain, default=Block.serialize_block))
    # print(bc.pub_key.public_bytes(encoding="UTF-8", format="JSON"))


    # print(bc.chain[0])
    # print(bc.chain[1]["Block"])
    # hash_of_second_block = bc.chain[1]["BlockHash"]
    # print(bc.get_block_with_hash(hash_of_second_block).previous_hash)
    # print(bc.validate_blockchain(bc.chain))
    # print(bc.owners_ip)