# constant product automated market maker arbitraage bot with ML

This project aims to show that short term patterns in our Automated Market Maker's (AMM) reserve balances, price differences, and recent swapping volumes contain signals to predict when a price divergence between our pool and a reference pool will exceed the fees.

This repository contains a minimal constant product AMM written in Solidity, along with Python scripts and Foundry tests to deploy, interact with, and validate its behavior on local Anvil node and also on Sepolia testnet. The Solidity smart contracts (cpamm.sol and TestToken.sol) are tested locally with Foundry Anvil to ensure correct liquidity and swap mechanics are simulated before deployment on the mainnet. 

Clone the repo and install the dependencies in a Python virtual environment (requirements.txt will be added later) and use Foundry for smart contract compilation and testing. Populate your .env file with your RPC endpoint and private key (either from one of the test addresses you get with Anvil with running "anvil &" or directly from Sepolia), then run "forge test" to verify the contracts on local.

The Python scripts in src automate the workflow. Run first, deploy_tokens.py compiles and deploys two mock ERC-20 tokens; next, deploy_cpamm.py deploys the AMM against those tokens and prints the contract address. Finally, generate_events.py simulates liquidity additions and swaps, and pulls all swapped events into data/raw_events dataset in .csv format for analysis.

In the upcoming days, this repository will add a Jupyter notebook for data labeling and classifier model training, a Python script that uses the trained classifier to decide when to execute arbitrage trades, and backtesting tools to evaluate the strategy's performance under different market conditions.
