# PyCoin

What is PyCoin?

Its a (work in progress) library to create and test small scale cryptocurrencies. It includes proof of work, hashing and the blockchain.
Unfortunately, the library does not yet have a node and consensus system, though it can be implemented alongside the library

So how do I start this anyways?

```
blockchain = Blockchain("Coin-Name", 4, "public_address")

blockchain.load_local_ledger()
blockchain.calculate_wallet("0")
blockchain.start_mine()
```
