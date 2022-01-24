This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
Built using [truffle suite react box](https://www.trufflesuite.com/boxes/react)

# Axolittles Subgraph Project
Developing a [subgraph](https://thegraph.com/en/) to keep track of Axolittles holders.

#### This was copied from another project of Toast's
Safely ignore most everthing in the `client/` directory, the frontend piece of this react box is not intended to be used here.

## Running Dev Stack with Truffle

### Install stuff
```
npm install
```

### Deploy the smart contract to local private blockchain
```
$truffle develop
truffle(develop)> migrate
```

### Mint some axos
script set up to mint axos `mint.py`.

## Graph Database
KELP app uses the graph protocol to index on-chain data into a graphql backend. That code lives in [`/subgraph/kelptoken/`](/subgraph/kelptoken/)


## Mint KELP
Using web3 (python):
```
python mint.py --to <recipient address> --grams-biomass <integer>
```
enter "y" when prompted to confirm the transaction.
