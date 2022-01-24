import json
import os
import argparse
import datetime
from util import get_contract

from web3 import Web3
import web3
from web3.middleware import construct_sign_and_send_raw_middleware
import pandas as pd
import numpy as np
from mint import mint_kelp_local
    
contract_address = '0x08DEEfCcC7f0C63b22fBE5D6C4bef795041551A5'
owner_address = "0x71267FBddE07E4a66c897ff05BaBCAe141FE9d88"
provider_address = 'http://localhost:8545'

if __name__ in "__main__":
    good = True
    if good:

        w3 = Web3(Web3.HTTPProvider(provider_address))
        contract = get_contract('./client/src/contracts/KelpToken.json', contract_address, w3)

        bene = w3.eth.accounts[0]
        #mass = int(np.random.randint(1000000000, 1000000000000))
        mass = 10000
        print('Minting kelp for: ', bene, ' carbon amount: ', mass)
        mint_success = mint_kelp_local(mass, bene, contract=contract, contract_address=contract_address)
        print('mint success: ', mint_success)


        for acct in w3.eth.accounts[1:]:
            amount = int(np.random.randint(10000000, 10000000000))
            print('want to send: ', amount, ' plankton to: ', acct)
            success = str(contract.functions.transfer(acct, amount).transact({"from":w3.eth.accounts[0]}))
            print("success: ", success)

