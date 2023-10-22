#!/usr/bin/env python3
import os
from BlockChain import Blockchain
import asyncio
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple argparse example.")
    parser.add_argument("-i", "--id", help="first user id", type=str)
    args = parser.parse_args()

    bc = Blockchain(args.id)
    print(bc.users_ips)
    asyncio.run(bc.run_all())
  
