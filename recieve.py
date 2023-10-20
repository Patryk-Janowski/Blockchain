from BlockChain import Blockchain
import time

if __name__ == "__main__":
    bc1 = Blockchain(1)
    bc1.listen_for_blocks()
    print(bc1.chain)
    print(bc1.users)

