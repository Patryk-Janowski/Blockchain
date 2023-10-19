import os
from BlockChain import Blockchain


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
    bc.create_block("xd")
    bc.create_block("hehehe")
    serialized_chain = bc.serialize_chain()
    deserialized_chain = bc.deserialize_chain(serialized_chain)
    print(bc.chain[1]["Block"])
    print(bc.users)
    print(bc.owners_ips)
