---
title: Basic Web3 Scripting in Python
tags:
  - python
---

# Basic Web3 Scripting in Python

I've often wished I had a simple python class to do ERC20 and ERC721 operations.

I sort of built that today for a script we needed to transfer a bunch of USDC tokens from a csv file to a single wallet.

Some obvious room for improvements, but this is what we got.

## Main script

```python
from typing import Any
import csv
import json
from eth_typing.encoding import HexStr
from web3 import Web3
from eth_account import Account

CONFIG: dict[str, dict[str, Any]] = {
    "mainnet": {
        "id": 1,
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "rpc": "https://mainnet.infura.io/v3/be126c2b281f43549f1ddc020fdcaee9",
    },
    "goerli": {
        "id": 5,
        "USDC": "0xD87Ba7A50B2E7E660f678A895E4B72E7CB4CCd9C",
        "rpc": "https://goerli.infura.io/v3/be126c2b281f43549f1ddc020fdcaee9",
    },
}

NETWORK = "mainnet"
DESTINATION_ADDRESS = "0x915d327bF740aA5C463e4ED07f7dfd775dd0993E"


class Erc20:
    abi_filename = "abi/erc20.json"

    def __init__(self, w3: Web3, token_address: str) -> None:
        with open(self.abi_filename) as fh:
            abi = json.load(fh)

        self.w3 = w3
        self.contract = self.w3.eth.contract(
            address=Web3.toChecksumAddress(token_address), abi=abi
        )
        self.chain_id = CONFIG[NETWORK]["id"]

    def balance_of(self, addr: str) -> int:
        cksum_addr = Web3.toChecksumAddress(addr)
        return self.contract.functions.balanceOf(cksum_addr).call()

    def tx_params(self, sender: Account) -> dict:
        nonce = self.w3.eth.get_transaction_count(sender.address)
        return {
            "gas": 850000,
            "nonce": nonce,
            "chainId": self.chain_id,
        }

    def transfer(self, sender: Account, to: str, amount: int) -> None:
        print(f"Starting transfer of {amount} to {to} from {sender.address}")
        cksum_addr = Web3.toChecksumAddress(to)
        tx_params = self.tx_params(sender)
        tx = self.contract.functions.transfer(cksum_addr, amount).buildTransaction(
            tx_params
        )

        signed_tx = self.w3.eth.account.sign_transaction(
            tx, private_key=sender.key.hex()
        )

        tx_hash: HexStr = self.w3.toHex(
            self.w3.keccak(signed_tx.rawTransaction)  # type: ignore
        )
        print(f"Transaction hash: {tx_hash}")
        self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        res = self.w3.eth.wait_for_transaction_receipt(signed_tx.rawTransaction)
        print(f"Result from transaction: {res}")


class Processor:
    def __init__(self) -> None:
        self.network = NETWORK
        token_addr = CONFIG[self.network]["USDC"]
        w3 = Web3(Web3.HTTPProvider(CONFIG[self.network]["rpc"]))
        self.token = Erc20(w3, token_addr)

    def process_wallet(self, wallet: Account):
        print(f"Processing wallet: {wallet.address}")
        balance = self.token.balance_of(wallet.address)
        print(f"Wallet has balance: {balance}")

        # TODO:
        # if balance > 0:
        #     self.token.transfer(wallet, DESTINATION_ADDRESS, 2)
        # self.token.transfer(wallet, DESTINATION_ADDRESS, amount)

    def load_wallets(self, filename: str) -> list[Account]:
        # Can do account.addres to get address even though pylance says you can't.
        with open(filename) as file_handle:
            accounts = []
            reader = csv.reader(file_handle)
            for row in reader:
                account = Account.from_key(row[1])
                accounts.append(account)
        return accounts

    def go(self) -> None:
        filename = "wallets.csv"
        wallets = self.load_wallets(filename)

        wallets = wallets[4:8]

        for i, wallet in enumerate(wallets):
            print(f"Loop: {i}, {wallet.address}")
            self.process_wallet(wallet)


Processor().go()
```

## Other files

### ERC20 ABI

```
[
  {
      "constant": true,
      "inputs": [],
      "name": "name",
      "outputs": [
          {
              "name": "",
              "type": "string"
          }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
  },
  {
      "constant": false,
      "inputs": [
          {
              "name": "_spender",
              "type": "address"
          },
          {
              "name": "_value",
              "type": "uint256"
          }
      ],
      "name": "approve",
      "outputs": [
          {
              "name": "",
              "type": "bool"
          }
      ],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
  },
  {
      "constant": true,
      "inputs": [],
      "name": "totalSupply",
      "outputs": [
          {
              "name": "",
              "type": "uint256"
          }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
  },
  {
      "constant": false,
      "inputs": [
          {
              "name": "_from",
              "type": "address"
          },
          {
              "name": "_to",
              "type": "address"
          },
          {
              "name": "_value",
              "type": "uint256"
          }
      ],
      "name": "transferFrom",
      "outputs": [
          {
              "name": "",
              "type": "bool"
          }
      ],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
  },
  {
      "constant": true,
      "inputs": [],
      "name": "decimals",
      "outputs": [
          {
              "name": "",
              "type": "uint8"
          }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
  },
  {
      "constant": true,
      "inputs": [
          {
              "name": "_owner",
              "type": "address"
          }
      ],
      "name": "balanceOf",
      "outputs": [
          {
              "name": "balance",
              "type": "uint256"
          }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
  },
  {
      "constant": true,
      "inputs": [],
      "name": "symbol",
      "outputs": [
          {
              "name": "",
              "type": "string"
          }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
  },
  {
      "constant": false,
      "inputs": [
          {
              "name": "_to",
              "type": "address"
          },
          {
              "name": "_value",
              "type": "uint256"
          }
      ],
      "name": "transfer",
      "outputs": [
          {
              "name": "",
              "type": "bool"
          }
      ],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
  },
  {
      "constant": true,
      "inputs": [
          {
              "name": "_owner",
              "type": "address"
          },
          {
              "name": "_spender",
              "type": "address"
          }
      ],
      "name": "allowance",
      "outputs": [
          {
              "name": "",
              "type": "uint256"
          }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
  },
  {
      "payable": true,
      "stateMutability": "payable",
      "type": "fallback"
  },
  {
      "anonymous": false,
      "inputs": [
          {
              "indexed": true,
              "name": "owner",
              "type": "address"
          },
          {
              "indexed": true,
              "name": "spender",
              "type": "address"
          },
          {
              "indexed": false,
              "name": "value",
              "type": "uint256"
          }
      ],
      "name": "Approval",
      "type": "event"
  },
  {
      "anonymous": false,
      "inputs": [
          {
              "indexed": true,
              "name": "from",
              "type": "address"
          },
          {
              "indexed": true,
              "name": "to",
              "type": "address"
          },
          {
              "indexed": false,
              "name": "value",
              "type": "uint256"
          }
      ],
      "name": "Transfer",
      "type": "event"
  }
]
```

### wallets.csv

```
address,private_key
0x123,456...
```

### pyproject.toml

This version is overkill.

```
[tool.poetry]
name = "web3 erc20"
version = "0.1.0"
description = ""
authors = ["Alex Ledger"]

[tool.poetry.dependencies]
python = "^3.10"
web3 = "5.25.0"
pyyaml = "5.4.1"
eth_account = "^0.5.6"
requests = "2.27.1"
python-multipart = "^0.0.5"
types-PyYAML = "^6.0.9"
types-requests = "^2.28.0"
pydantic = "^1.9.1"

[tool.poetry.dev-dependencies]
coverage = "5.0.4"
flake8 = "3.7.9"
flake8-annotations = "2.1.0"
Sphinx = "4.4.0"
pytest = "^7.0.0"
tox = "3.24.4"
black = "^22.3.0"
isort = "^5.10.1"
mypy = "^0.961"
pylint = "2.13.9"

[tool.isort]
profile = "black"
```
