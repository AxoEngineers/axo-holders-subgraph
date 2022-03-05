from tracemalloc import start
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import json
import numpy as np
import argparse
import time


transport = AIOHTTPTransport(url="https://api.studio.thegraph.com/query/19838/axolittles/v0.0.85")
client = Client(transport=transport, fetch_schema_from_transport=True)
emission_v1 = 15000000000000000
deploy_block = 13171333
n8_block = 13949318
first_airdrop_block = 14169463

#############################
#graph queries and utilities#
#############################

holder_query = gql(
"""
query getHistory($address: ID!) {
  axoHolder(id: $address) {
    toTransfer(first: 1000) {
      from {
        id
      }
      to {
        id
      }
      token_id
      blockHeight
    }
    fromTransfer(first: 1000) {
      from {
        id
      }
      to {
        id
      }
      token_id
      blockHeight
    }
  }
}
"""
)

def query_holder_history(address):
    params = {"address": address.lower()}
    result = client.execute(query, variable_values=params)
    return result


holder_query = gql(
"""
query getHolders($startBlock: BigInt!, $stopBlock: BigInt!, $skip: Int) 
{
  axoHolders(first:1000 skip:$skip where: {lastActiveBlock_lt:$stopBlock, lastActiveBlock_gt: $startBlock}) {
    id
  }
}
"""
)

def get_all_holders(final_stop_block, verbose=True):
    """
    This will get all the axoHolder addresses.
    returns a set of strings.
    """
    start_block = 13171332
    skip = 0
    proceed = True
    output = set()
    while (start_block < final_stop_block) & proceed:
        stop_block = start_block + 2500
        if verbose:
          print(f'running for blocks: {start_block}, {stop_block}')
        params = {"startBlock": str(start_block-1), "stopBlock": str(stop_block+1), "skip":skip}
        result = client.execute(holder_query, variable_values=params)
        if verbose:
          print('got: ', len(result['axoHolders']), 'holders.')
        assert len(result['axoHolders']) < 1000
        output = output.union(set([x['id'] for x in result['axoHolders']]))
        start_block = stop_block

    return output

snapshot_query = gql(
"""
query getHolderAtBlock($blockHeight: Int!, $address: ID!) 
{
  axoHolder(id: $address block: { number: $blockHeight }) {
    axosHeld(first:1000) {
      id
    }
    axosStakedV1(first:1000) {
      id
    }
    axosStakedV2Test(first:1000) {
      id
    }
    axosStakedV2(first:1000) {
      id
    }
  }
}
"""
)

def get_count_at_block(
        address, 
        block=14112091
      ):
    """
    This will get the axo counts for address at block.
    returns (n_axos, n_axosStakedV1, n_axosStakedV2)
    """
    params = {"blockHeight":block, "address":address.lower()}
    result = client.execute(snapshot_query, variable_values=params)
    if result['axoHolder'] is None:
      return 0, 0, 0
    else:
      holder = result['axoHolder']
      return len(holder['axosHeld']), len(holder['axosStakedV1']), len(holder['axosStakedV2'])

claim_query = gql(
"""
query getClaims($address: ID!, $stopBlock: BigInt!) {
  axoHolder(id: $address) {
    id
    claimedBubble (where: { blockHeight_lt: $stopBlock }) {
      amount
      blockHeight
    }
}
}

"""
)

def get_claims_for_user(address, stopBlock):
  """
  this will return a list of all the blocks when a user claimed $bubble
  on the v1 contract.
  """
  params = {
    "address":address.lower(),
    "stopBlock":int(stopBlock+1)
    }
  result = client.execute(claim_query, variable_values=params)
  claims = result['axoHolder']['claimedBubble']
  amounts = np.array([int(x['amount']) for x in claims])
  blocks = np.array([int(x['blockHeight']) for x in claims])
  indices = np.argsort(blocks)
  blocks = blocks[indices]
  amounts = amounts[indices]
  return blocks, amounts

def get_total_claimed(address, stopBlock):
  """
  returns the total amount of $bubble
  claimed by address.
  """
  _, amounts = get_claims_for_user(address, stopBlock)
  return sum(amounts)

airdrop_claim_query = gql(
"""
query getAirdropClaims($address: ID!, $stopBlock: BigInt!) {
  axoHolder(id: $address) {
    id
    claimedAirdrops (where: { blockHeight_lt: $stopBlock }) {
      amount
    }
}
}

"""
)

def get_airdrop_claims_for_user(address, stopBlock):
  """
  this will return a list of all the blocks when a user claimed $bubble
  from an airdrop.
  """
  params = {
    "address":address.lower(),
    "stopBlock":int(stopBlock+1)
    }
  result = client.execute(airdrop_claim_query, variable_values=params)
  claims = result['axoHolder']['claimedAirdrops']
  amounts = np.array([int(x['amount']) for x in claims])
  return amounts

def get_total_airdrop_claimed(address, stopBlock):
  """
  returns the total amount of $bubble
  claimed from airdrops.
  """
  amounts = get_airdrop_claims_for_user(address, stopBlock)
  return sum(amounts)

activity_query = gql(
"""
query getActivity($address: ID!) {
  axoHolder(id: $address) {
    toTransfer(first:1000) {
      blockHeight
    }
    fromTransfer(first:1000) {
      blockHeight
    }
  }
}
"""
)

def get_all_active_blocks(address):
  """
  this will return a list of all the active blocks for a user.
  """
  params = {"address":address.lower()}
  result = client.execute(activity_query, variable_values=params)
  holder = result['axoHolder']
  blocks = []
  for item in holder['fromTransfer']:
    blocks.append(item['blockHeight'])
  for item in holder['toTransfer']:
    blocks.append(item['blockHeight'])
  result = list(set(blocks))
  result = [int(x) for x in result]
  return sorted(result)

txn_query = gql(
    """
query getTxns($address: ID!) {
  axoHolder(id: $address) {
    toTransfer(first: 1000) {
      from {
        id
      }
      to {
        id
      }
      token_id
      blockHeight
    }
    fromTransfer(first: 1000) {
      from {
        id
      }
      to {
        id
      }
      token_id
      blockHeight
    }
  }
}
"""
)

def get_transaction_history(address):
    params = {"address": address.lower()}
    return client.execute(txn_query, variable_values=params)

#############################
#batch functions and scripts#
#############################

def parse_axotime(
        data, 
        owner_address, 
        staking_address="0x1cA6e4643062e67CCd555fB4F64Bee603340e0ea".lower(),
        staking_v2_address="0xfa822d611e583a6fb879c03645ddfd1c8877252a".lower(),
        void_address="0x0000000000000000000000000000000000000000".lower()
    ):
    """
    Parses the Transfer() events emitted
    for `owner_address` into a sequence of
    blocks with acquisition, loss, stake, and unstaking token ids.
    returns a dictionary
    """
    blocks = {}
    holder = data['axoHolder']
    
    for item in holder['fromTransfer']:
        token = item['token_id']
        block_height = item['blockHeight']
        block_data = blocks.get(block_height)
        if block_data is None:
            block_data = {
            "tokens_staked":[],
            "tokens_unstaked":[],
            "tokens_staked_v2":[],
            "tokens_unstaked_v2":[],
            "tokens_acquired":[],
            "tokens_lost":[]
        }
        
        try:
            assert item['from']['id'] == owner_address
        except AssertionError:
            msg = "data has reached an unexpected state."
            msg += " in fromTransfer event, 'from' addy is not owner addy"
        if item['to']['id'] == staking_address:
            #count as staked
            #print(f'staked token {token} at block {block_height}')
            block_data['tokens_staked'].append(token)
        elif item['to']['id'] == staking_v2_address:
            #count as staked
            #print(f'staked token {token} at block {block_height}')
            block_data['tokens_staked_v2'].append(token)
        else:
            #print(f'lost token {token} at block {block_height}')
            pass
        block_data['tokens_lost'].append(token)
        blocks[block_height] = block_data
            
    for item in holder['toTransfer']:
        token = item['token_id']
        block_height = item['blockHeight']
        block_data = blocks.get(block_height)
        if block_data is None:
            block_data = {
            "tokens_staked":[],
            "tokens_unstaked":[],
            "tokens_staked_v2":[],
            "tokens_unstaked_v2":[],
            "tokens_acquired":[],
            "tokens_lost":[]
        }
        
        try:
            assert item['to']['id'] == owner_address
        except AssertionError:
            msg = "data has reached an unexpected state."
            msg += " in toTransfer event, 'to' addy is not owner addy"
        if item['from']['id'] == staking_address:
            #count as staked
            #print(f'unstaked token {token} at block {block_height}')
            block_data['tokens_unstaked'].append(token)
        elif item['from']['id'] == staking_v2_address:
            #count as staked
            #print(f'unstakedv2 token {token} at block {block_height}')
            block_data['tokens_unstaked_v2'].append(token)
        elif item['from']['id'] == void_address:
            #print(f'minted token {token} at block {block_height}')
            pass
        else:
            #print(f'got token {token} at block {block_height}')
            pass
        block_data['tokens_acquired'].append(token)
            
        blocks[block_height] = block_data
        

    ordered_blocks = []
    for block in blocks:
        struct = {
            "block":block,
            "data":blocks[block]
        }
        ordered_blocks.append(struct)
    ordered_blocks.sort(key=lambda x: int(x['block']))
    return ordered_blocks

def counts_over_time(ordered_blocks):
    bag_o_axos = set()
    axovault = set()
    total_count = []
    for block in ordered_blocks:
        if len(total_count) == 0:
            total = {
                "block":block['block'],
                "axo_count":0,
                "staked_count":0,
                "staked_v2_count":0
            }
        else:
            total = total_count[-1].copy()
        total['block'] = int(block['block'])
        data = block['data']
        total['axo_count'] += len(data['tokens_acquired']) - len(data['tokens_lost'])
        #print(bag_o_axos)
        bag_o_axos = bag_o_axos.union(set(data['tokens_acquired']))
        # try:
        #     assert set(data['tokens_lost']).issubset(bag_o_axos)
        # except:
        #     raise Exception(set(data['tokens_lost']) - bag_o_axos)
        bag_o_axos = bag_o_axos - set(data['tokens_lost'])
        #print(bag_o_axos)
        total['staked_count'] += len(data['tokens_staked']) - len(data['tokens_unstaked'])
        total['staked_v2_count'] += len(data['tokens_staked_v2']) - len(data['tokens_unstaked_v2'])

        total_count.append(total)
    return total_count

def get_claimable_axotime_before_n8(_history, n8_block=13949318):
    axotime = 0
    exit = False
    for i, item in enumerate(_history[:-1]):
        _time = _history[i+1]["block"] - item["block"]
        if (_history[i+1]["block"] >= n8_block):
            #case when next state is after n8_block
            _time = n8_block - item["block"]
            exit = True
        count = item["staked_count"]
        axotime += int(_time) * int(count)
        if exit:
            return axotime
    #case when state hasn't updated since n8_block
    stop_state = _history[-1]
    _time = n8_block - stop_state["block"]
    count = stop_state["staked_count"]
    axotime += int(_time) * int(count)
    return axotime

def get_claimable_axotime_after_n8(_history, n8_block=13949318, stop_block=14169040):
    axotime = 0
    exit = False
    active_blocks = [x["block"] for x in _history]
    if max(active_blocks) <= n8_block:
        state = _history[-1]
        count = state["staked_count"] + state["axo_count"] + state["staked_v2_count"]
        _time = stop_block - n8_block
        axotime += _time * count
        return axotime
    elif min(active_blocks) >= n8_block:
        start_state = {
          'block': n8_block, 
          'axo_count': 0, 
          'staked_count': 0, 
          'staked_v2_count': 0
          }
        _history = [start_state] + _history
    else:
        diffs = n8_block - np.array(active_blocks)
        diffs = np.where(diffs<0, np.inf, diffs)
        start_state_index = np.argmin(diffs)
        start_state = _history[start_state_index].copy()
        start_state["block"] = n8_block
        _history = [start_state] + _history[(start_state_index+1):]
    active_blocks = [x["block"] for x in _history]
    diffs = stop_block - np.array(active_blocks)
    diffs = np.where(diffs<0, np.inf, diffs)
    stop_state_index = np.argmin(diffs)
    stop_state = _history[stop_state_index].copy()
    stop_state["block"] = stop_block
    _history = _history[:(stop_state_index+1)] + [stop_state]
    for i, state in enumerate(_history[:-1]):
        _count = state["staked_count"] + state["axo_count"] + state["staked_v2_count"]
        _time = _history[i+1]["block"] - state["block"]
        axotime += _count * _time
    return axotime

def get_claimable_axotime_after_first_airdrop(_history, first_airdrop_block=first_airdrop_block, stop_block=14169040):
    axotime = 0
    exit = False
    active_blocks = [x["block"] for x in _history]
    if max(active_blocks) <= first_airdrop_block:
        state = _history[-1]
        count = state["staked_count"]
        _time = stop_block - first_airdrop_block
        axotime += _time * count
        return axotime
    elif min(active_blocks) >= first_airdrop_block:
        start_state = {
          'block': first_airdrop_block, 
          'staked_count': 0
          }
        _history = [start_state] + _history
    else:
        diffs = first_airdrop_block - np.array(active_blocks)
        diffs = np.where(diffs<0, np.inf, diffs)
        start_state_index = np.argmin(diffs)
        start_state = _history[start_state_index].copy()
        start_state["block"] = first_airdrop_block
        _history = [start_state] + _history[(start_state_index+1):]
    active_blocks = [x["block"] for x in _history]
    diffs = stop_block - np.array(active_blocks)
    diffs = np.where(diffs<0, np.inf, diffs)
    stop_state_index = np.argmin(diffs)
    stop_state = _history[stop_state_index].copy()
    stop_state["block"] = stop_block
    _history = _history[:(stop_state_index+1)] + [stop_state]
    for i, state in enumerate(_history[:-1]):
        _count = state["staked_count"]
        _time = _history[i+1]["block"] - state["block"]
        axotime += _count * _time
    return axotime

def compute_first_airdrop(startBlock=13949318, stopBlock=14169277, verbose=True):
    print('computing airdrop for start block: ', startBlock, ' and stopBlock: ', stopBlock)
    output = []
    ngmi = []
    with open('./holders.json', 'r') as f:
        inp = json.loads(f.read())
        print('got: ', len(inp), ' total holder addresses.')
    output = []
    print('running for: ', len(inp), ' remaining addresses.')
    for i, address in enumerate(inp):
        #time.sleep(0.01)
        if verbose:
            print(round(100*i/len(inp), 4), "percent complete.")
        success = False
        while not success:
            try:
                _history = get_transaction_history(address)
                _history = parse_axotime(_history, address)
                _history = counts_over_time(_history)
                axotime = get_claimable_axotime_before_n8(_history, n8_block=startBlock)
                axotime += get_claimable_axotime_after_n8(_history, n8_block=startBlock, stop_block=stopBlock)
                total_claimable = int(axotime) * emission_v1
                total_claimed = get_total_claimed(address.lower(), stopBlock)
                airdrop_total = total_claimable - total_claimed
                success = True
            except Exception as e:
                print('failed with: ', str(e))
                print('cooling down for 60 seconds...')
                time.sleep(60)

        entry = {
          "address":address,
          "balance":str(airdrop_total)
        }
        if airdrop_total > 0:
            output.append(entry)
            if verbose:
                print(entry)
                print('writing to airdrop.json...')
            with open('./airdrop.json', 'w') as f:
                f.write(json.dumps(output))
            if verbose:
                print('done!')
        else:
            ngmi.append(entry)
            if verbose:
                print(entry)
                print('got zero balance.')
                print('writing to ngmi.json...')
            with open('./ngmi.json', 'w') as f:
                f.write(json.dumps(ngmi))
            if verbose:
                print('done!')


def compute_later_airdrop(stopBlock=14324006, verbose=True):
    print('computing airdrop for stopBlock: ', stopBlock)
    output = []
    ngmi = []
    with open('./holders.json', 'r') as f:
        inp = json.loads(f.read())
        print('got: ', len(inp), ' total holder addresses.')
    with open('./first_airdrop.json', 'r') as f:
        first_airdrop = json.loads(f.read())
        first_airdrop_indexed = {}
        for item in first_airdrop:
            first_airdrop_indexed[item['address']] = item['balance']
        first_airdrop = first_airdrop_indexed
        print('got: ', len(first_airdrop), ' addresses from first_airdrop.json')
    output = []
    print('running for: ', len(inp), ' remaining addresses.')
    for i, address in enumerate(inp):
        #time.sleep(0.01)
        if verbose:
            print(round(100*i/len(inp), 4), "percent complete.")
        success = False
        while not success:
            try:
                _history = get_transaction_history(address)
                _history = parse_axotime(_history, address)
                _history = counts_over_time(_history)
                #axotime = get_claimable_axotime_before_n8(_history, n8_block=startBlock)
                axotime = get_claimable_axotime_after_first_airdrop(_history, stop_block=stopBlock)
                total_claimable = int(axotime) * emission_v1
                #add in first airdrop balance
                first_airdrop_claimable = int(first_airdrop.get(address, 0))
                #subtract total claimed airdrop balance
                total_claimed_airdrop = get_total_airdrop_claimed(address.lower(), stopBlock)
                airdrop_total = first_airdrop_claimable + total_claimable - total_claimed_airdrop
                success = True
            except Exception as e:
                print('failed with: ', str(e))
                print('cooling down for 60 seconds...')
                time.sleep(60)

        entry = {
          "address":address,
          "balance":str(airdrop_total)
        }
        if airdrop_total > 0:
            output.append(entry)
            if verbose:
                print(entry)
                print('writing to airdrop.json...')
            with open('./airdrop.json', 'w') as f:
                f.write(json.dumps(output))
            if verbose:
                print('done!')
        else:
            ngmi.append(entry)
            if verbose:
                print(entry)
                print('got zero balance.')
                print('writing to ngmi.json...')
            with open('./ngmi.json', 'w') as f:
                f.write(json.dumps(ngmi))
            if verbose:
                print('done!')

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stopBlock", type=int,
                        help="the up-until blockHeight for the airdrop.")
    parser.add_argument("--verbose", action="store_true",
                        help="if you want to spam logs into your console")
    args = parser.parse_args()
    return args

def main():
    print('running airdrop script...')
    args = parse_args()
    stop_block = args.stopBlock
    verbose = args.verbose
    print('using stopBlock: ', stop_block)
    print('getting all axoHolders...')
    result = get_all_holders(stop_block, verbose=verbose)
    print('done!')
    with open('holders.json', 'w') as f:
        print('got: ', len(list(result)), " holders.")
        f.write(json.dumps(list(result)))
    print('computing airdrop balances...')
    compute_later_airdrop(stopBlock=stop_block, verbose=verbose)
    print('done! exiting...')
    quit()

#airdrop = airdrop1 + airdropx - airdropClaimAmount

if __name__ in "__main__":
    main()
    #print(get_count_at_block("0x4F17562C9a6cCFE47c3ef4245eb53c047Cb2Ff1D", 14181249))
    # toast_address = "0x4f17562c9a6ccfe47c3ef4245eb53c047cb2ff1d"
    # print(get_total_airdrop_claimed(toast_address, 14324006))
