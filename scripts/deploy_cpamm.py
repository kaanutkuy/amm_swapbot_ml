import os
from dotenv import load_dotenv
from web3 import Web3
import solcx
from solcx import compile_standard, install_solc

load_dotenv()

rpc_url     = os.getenv("RPC_URL")
private_key = os.getenv("PRIVATE_KEY")
token0_addr = os.getenv("TOKEN0_ADDRESS")
token1_addr = os.getenv("TOKEN1_ADDRESS")

w3 = Web3(Web3.HTTPProvider(rpc_url))
assert w3.is_connected(), "Cannot connect to Sepolia"

install_solc('0.8.30')
with open('contracts/cpamm.sol', 'r') as f:
    source = f.read()

compiled = compile_standard(
    input_data={
    "language": "Solidity",
    "sources": {"AMM.sol": {"content": source}},
    "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}}},
    solc_version='0.8.30'
    )
abi = compiled['contracts']['AMM.sol']['AMM']['abi']
bytecode = compiled['contracts']['AMM.sol']['AMM']['evm']['bytecode']['object']

# contract
acct = w3.eth.account.from_key(private_key)
AMM = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(acct.address)

# deployment transaction
transaction = AMM.constructor(
    token0_addr,
    token1_addr
).build_transaction({
    'from': acct.address,
    'nonce': nonce,
    'gasPrice': w3.eth.gas_price,
    'chainId': w3.eth.chain_id
})

signed_transaction = acct.sign_transaction(transaction)
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.raw_transaction)

print(f"Deployment transaction hash: {transaction_hash.hex()}")
receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
print(f"Constant Product AMM deployed at: {receipt.contractAddress}")