import os
from BlockChain import Blockchain
import asyncio

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
    bc = Blockchain("XD", "255.255.255.255")
    asyncio.run(bc.run_all())
  
