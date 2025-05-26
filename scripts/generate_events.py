import os
from dotenv import load_dotenv
from web3 import Web3
import pandas as pd
import json

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
acct = w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))
nonce = w3.eth.get_transaction_count(acct.address)

with open("out/cpamm.sol/AMM.json") as f:
    contract_json = json.load(f)
    amm_abi = contract_json["abi"]

amm = w3.eth.contract(address=os.getenv("AMM_ADDRESS"), abi=amm_abi)

with open("out/TestToken.sol/TestToken.json") as f:
    token_json = json.load(f)
    token_abi  = token_json["abi"]
token0 = w3.eth.contract(address=os.getenv("TOKEN0_ADDRESS"), abi=token_abi)
token1 = w3.eth.contract(address=os.getenv("TOKEN1_ADDRESS"), abi=token_abi)

# produce some events: add liquidity & a few swaps
def send_tx(fn, *args):
    global nonce
    tx = fn(*args).build_transaction({
        "from":     acct.address,
        "nonce":    nonce,
        "gasPrice": w3.eth.gas_price,
        "chainId":  w3.eth.chain_id
    })
    signed = acct.sign_transaction(tx)
    txh = w3.eth.send_raw_transaction(signed.raw_transaction)
    w3.eth.wait_for_transaction_receipt(txh)
    nonce += 1
    
send_tx(token0.functions.approve, os.getenv("AMM_ADDRESS"), 10**24)
send_tx(token1.functions.approve, os.getenv("AMM_ADDRESS"), 10**24)

# add liquidity once
send_tx(amm.functions.addLiquidity, 10**20, 10**20)

# do 5 swaps alternating token0→token1 and back
for i in range(5):
    send_tx(amm.functions.swap, os.getenv("TOKEN0_ADDRESS"), 10**18)
    send_tx(amm.functions.swap, os.getenv("TOKEN1_ADDRESS"), 10**18)

# fetch all Swap events
#events = amm.events.Swapped.createFilter(fromBlock=0, toBlock="latest").get_all_entries()

# pull all logs from the AMM address
logs = w3.eth.get_logs({
    "fromBlock": 0,
    "toBlock": "latest",
    "address": os.getenv("AMM_ADDRESS"),
    "topics": [w3.keccak(text="Swapped(address,address,uint256,uint256)").hex()]
})

events = [amm.events.Swapped().process_log(log) for log in logs]

rows = []
for e in events:
    rows.append({
        "blockNumber":  e.blockNumber,
        "trader":       e.args.trader,
        "tokenIn":      e.args.tokenIn,
        "amountIn":     e.args.amountIn,
        "amountOut":    e.args.amountOut
        })

df = pd.DataFrame(rows)
df.to_csv("data/raw_events.csv", index=False)
print("Wrote", len(df), "swap events to data/raw_events.csv")
