import os
from dotenv import load_dotenv
from web3 import Web3
import solcx
from solcx import compile_standard, install_solc, get_installable_solc_versions

load_dotenv()

rpc_url     = os.getenv("RPC_URL")
private_key = os.getenv("PRIVATE_KEY")

w3 = Web3(Web3.HTTPProvider(rpc_url))
assert w3.is_connected(), "Cannot connect to Sepolia"

install_solc('0.8.30')
with open('contracts/TestToken.sol', 'r') as f:
    source = f.read()
    
compiled = compile_standard(
    input_data={
    "language": "Solidity",
    "sources": {"TestToken.sol": {"content": source}},
    "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}}},
    solc_version='0.8.30'
)
token_abi = compiled['contracts']['TestToken.sol']['TestToken']['abi']
token_bytecode = compiled['contracts']['TestToken.sol']['TestToken']['evm']['bytecode']['object']

acct = w3.eth.account.from_key(private_key)
Token = w3.eth.contract(abi=token_abi, bytecode=token_bytecode)
nonce = w3.eth.get_transaction_count(acct.address)

# token0
transaction0 = Token.constructor("Token0", "T0", 10**24).build_transaction({
    'from': acct.address, 
    'nonce': nonce,
    'gasPrice': w3.eth.gas_price, 
    'chainId': w3.eth.chain_id
})
signed0 = acct.sign_transaction(transaction0)
hash0 = w3.eth.send_raw_transaction(signed0.raw_transaction)
receipt0 = w3.eth.wait_for_transaction_receipt(hash0)

# token1
nonce += 1
transaction1 = Token.constructor("Token1", "T1", 10**24).build_transaction({
    'from': acct.address, 
    'nonce': nonce,
    'gasPrice': w3.eth.gas_price, 
    'chainId': w3.eth.chain_id
})
signed1 = acct.sign_transaction(transaction1)
hash1 = w3.eth.send_raw_transaction(signed1.raw_transaction)
receipt1 = w3.eth.wait_for_transaction_receipt(hash1)

print(f"Token0 at: {receipt0.contractAddress}")
print(f"Token1 at: {receipt1.contractAddress}")
