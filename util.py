from web3 import Web3
import web3
import json
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--truffle-abi-path", type=str,
                        help="path to truffle-generated abi blob")
    parser.add_argument("--output-path", type=str,
                        help="path to write out graph-compatible abi")
    args = parser.parse_args()
    return args

def get_contract(path, contract_address, w3, is_truffle=True):
    with open(path, 'r') as f:
        abi = json.loads(f.read())
    if is_truffle: #get abi out of greater truffle blob
        abi = abi['abi']

    contract = w3.eth.contract(address=contract_address, abi=abi)
    return contract

def extract_abi(input_path, output_path):
    with open(input_path, 'r') as f:
        abi = json.loads(f.read())['abi']
    
    with open(output_path, 'w') as f:
        f.write(json.dumps(abi))

    return True

if __name__ in "__main__":

    args = parse_args()
    input_path, output_path = args.truffle_abi_path, args.output_path
    extract_abi(input_path, output_path)