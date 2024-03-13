# Fight club script in Ethereum blobs

Publishes 2 blobs with the whole Fight club script with pruned spaces and unnecessary stuff & sends 2 txs that verify the first rule of fight club using point evaluation precompile (that is, onchain)

[Posted here](https://blobscan.com/tx/0xc5c2e96c9da3fdacc466dc7f239d1c0225764f47c46516e8599b5475b4be6043), proved [here](https://etherscan.io/tx/0x3e756844487fd1edc178b7f10975bf4488ab7cd18fd93b23421815595f362ea7) and [here](https://etherscan.io/tx/0xad6b77265406737f8980ddad5296ffa29b95b5d4a4e23ef395bd97ca76bb7381). The code is quite a mess partly because web3.py hasn't been upgraded to 4844 yet and partly because I wanna sleep af rn, maybe I'll rewrite it someday

# Usage

1. Install [c-kzg-4844 python bindings](https://github.com/ethereum/c-kzg-4844/tree/main/bindings/python) and web3.py
3. `export ETH_JSON_RPC=your EL JSON RPC`
4. `export ETH_PRIVATE_KEY=your private key`
5. `python3 publish.py`
6. `python3 prove.py`
