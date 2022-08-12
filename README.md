# Axolittles Subgraph Project
Developing a [subgraph](https://thegraph.com/en/) to keep track of Axolittles holders and the $bubble tokens they have earned.

## Graph Database
Graph protocol code lives in [`/subgraph/axolittles/`](/subgraph/axolittles/)


## Compute Airdrop
There are some python utilities here to compute airdrop balances. Note that these scripts make lots of network calls to the graph api (TODO - can we index the entire graph db locally?)

### setting up python env

```
mkdir ~/.venvs
python3 -m venv ~/.venvs/graphs
source ~/.venvs/graphs/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### running the airdrop script
Currently the airdrop logic has a hard-coded "n8_block" (`13949318`), the block when n8 announced a new plan for axolittles staking, and the "first_airdrop_block", which was the block when the first airdrop (which included $bubble for non-staked axos, `14169463`). The only parameter to this script is the `stopBlock`, which is the block at which you would like to take the snapshot (probably a very recent block). After setting up your python env, invoke the script with:

```
python get_airdrop.py --stopBlock 15329300 --verbose
```

add `--verbose` if you want moar logs.


the `airdrop.json` file should be written into the root of this repository. you will also get a `ngmi.json` file which contains all the zero-balance airdrops (wallets that once held axos that won't be able to claim any tokens in this drop.)

### March Airdrop
using block `14360173`

### Second March 2022 (bafc) Airdrop
using block `14472866`

### April 2022 Airdrop
using block `14673935`

### August Airdrop
using block `15329300`
