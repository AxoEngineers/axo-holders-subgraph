from web3 import Web3
import web3
from web3.middleware import construct_sign_and_send_raw_middleware
import json
import argparse
from util import get_contract
import numpy as np
    
contract_address = '0x5F6A7a501C74d2eb60F039e9D4Fb1c7C85ceB997'
#contract_address = '0x0c2aFA30bBc3AAB44d74b0be85c4E27B378aE719' #ropsten deploy2

provider_address = 'https://ropsten.infura.io/v3/e0612a9ac52d4e0ea8b800c5b24e48fb'


# owner = 0xB6115FfA40a9233d1d2A947E3585D7D9b15Ce012
# /home/alliedtoasters/miniconda3/envs/eth/bin/python mint.py --to 0xB6115FfA40a9233d1d2A947E3585D7D9b15Ce012 --grams-carbon 10000 --keystore /home/alliedtoasters/projects/kelp_app_fullstack/kelp_backend/keystore/owner --password test123

mint_price = 0.07
max_mint = 10

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", type=str,
                        help="to address")
    parser.add_argument("--keystore", type=str,
                        help="path to geth keystore file for owner account")
    parser.add_argument("--password", type=str,
                        help="password for geth keystore file")
    parser.add_argument('--yes', action='store_true')
    parser.add_argument("--n_mintings", type=int,
                        help="number of mint events to simulate.")
    args = parser.parse_args()
    return args

def mint_axos_local(
        contract=None,
        provider_address="http://localhost:7545", 
        contract_address=contract_address
        ):
    w3 = Web3(Web3.HTTPProvider(provider_address))
    if contract is None:
        contract = get_contract('/home/alliedtoasters/Desktop/nfts/axodevs/AxoHolderGraph/client/src/contracts/Axolittles.json', contract_address, w3)
    #doc_hash = w3.keccak(b'TEST DOC')
    minter = np.random.randint(10)
    n_axos_to_mint = np.random.randint(10)
    amount = n_axos_to_mint * mint_price
    success = str(contract.functions.publicMint().transact({"from":w3.eth.accounts[minter], "amount":amount}))
    return success


def pass_the_baby(
        contract=None,
        provider_address="http://localhost:8545", 
        contract_address=contract_address
        ):
    """
    Simulates people transfering axos to each other.
    doesn't work/wip
    """
    w3 = Web3(Web3.HTTPProvider(provider_address))
    if contract is None:
        contract = get_contract('/home/alliedtoasters/Desktop/nfts/axodevs/AxoHolderGraph/client/src/contracts/Axolittles.json', contract_address, w3)
    #doc_hash = w3.keccak(b'TEST DOC')
    sender = np.random.randint(10)
    reciever = np.random.randint(10)
    while reciever == sender:
        reciever = np.random.randint(10)
    amount = n_axos_to_mint * mint_price
    success = str(contract.functions.publicMint().transact({"from":w3.eth.accounts[minter], "amount":amount}))
    return success


def check_total_supply(
        contract=None,
        provider_address="http://localhost:8545", 
        contract_address=contract_address
        ):
    w3 = Web3(Web3.HTTPProvider(provider_address))
    if contract is None:
        contract = get_contract('/home/alliedtoasters/Desktop/nfts/axodevs/AxoHolderGraph/client/src/contracts/Axolittles.json', contract_address, w3)
    #doc_hash = w3.keccak(b'TEST DOC')
    #success = str(contract.functions.publicMint().transact({"from":w3.eth.accounts[0], "amount":1.0}))
    return contract.functions.totalSupply().transact({"from":w3.eth.accounts[0]})



if __name__ in "__main__":

    args = parse_args()
    recipient_address = args.to
    keystore_path = args.keystore
    pw = args.password
    yes = args.yes
    n_mintings = args.n_mintings
    print(f"You are about to simulate {n_mintings} minting events.")
    if not yes:
        resp = input("The axos are coming. Are you sure this information is correct? y/n\n")
    else:
        print('--yes passed as argument. proceeding...')
        resp = 'y'
    if resp.lower() == 'y':
        for i in range(n_mintings):
            print('minting...')
            status = mint_axos_local()
            print("got status: ")
            print(status)
        print(check_total_supply())
