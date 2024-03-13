import os, ckzg, rlp
from web3 import Web3
from eth_keys import KeyAPI
from hashlib import sha256

setup = ckzg.load_trusted_setup("trusted_setup.txt")

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def convert_into_blobs(data):
    padded_data = b""
    for chunk in chunks(data, 31):
        padded_data += b"\x00" + chunk
    
    blobs = []
    for chunk in chunks(padded_data, 131072):
        chunk += b"\x00" * (131072-len(chunk))
        blobs.append(chunk)
    
    return blobs

# web3.py doesn't yet support 4844 so it's really messy
def main():
    rpc = os.getenv("ETH_JSON_RPC")
    assert rpc, "missing ETH_JSON_RPC env variable"

    web3 = Web3(Web3.HTTPProvider(rpc))
    assert(web3.is_connected())

    print("connected to JSON RPC")

    private_key = os.getenv("ETH_PRIVATE_KEY")
    assert private_key, "missing ETH_PRIVATE_KEY env variable"
    address = web3.eth.account.from_key(private_key).address

    print("imported private key")

    blobs = convert_into_blobs(open("fightclub.txt", "rb").read())

    print("converted script into %d blobs" % len(blobs))

    blob = blobs[0]

    commitment = ckzg.blob_to_kzg_commitment(blob, setup)
    versioned_hash = b"\x01" + sha256(commitment).digest()[1:]

    element1 = blob[51744:51776]
    proof1 = ckzg.compute_kzg_proof(blob, element1, setup)
    element2 = blob[51776:51808]
    proof2 = ckzg.compute_kzg_proof(blob, element2, setup)

    print("computed two proofs")

    for element, proof in [(element1, proof1), (element2, proof2)]:
        calldata = versioned_hash + element + proof[1] + commitment + proof[0]
        raw_tx = [1, web3.eth.get_transaction_count(address), web3.eth.max_priority_fee, web3.eth.gas_price, 74072, bytes(19) + b"\x0a", 0, calldata, []]

        keys = KeyAPI()
        signature = keys.ecdsa_sign(web3.keccak(b"\x02" + rlp.encode(raw_tx)), keys.PrivateKey(bytes.fromhex(private_key[2:])))
        raw_tx.append(signature.v)
        raw_tx.append(signature.r)
        raw_tx.append(signature.s)
        tx = b"\x02" + rlp.encode(raw_tx)

        print("built tx")
    
        txid = web3.eth.send_raw_transaction(tx)
        print("sent", txid.hex())
        print(element[1:].decode())

    return

main()