import json

def decrypt_object(obj):
    # Your decryption logic here
    # For this example, we'll just return the input
    return obj

def decrypt_blockchain(chain):
    decrypted_chain = []
    for block in chain:
        decrypted_data = decrypt_object(block["data"])
        decrypted_block = {
            "index": block["index"],
            "timestamp": block["timestamp"],
            "data": decrypted_data,
            "previous_hash": block["previous_hash"],
            "hash": block["hash"]
        }
        decrypted_chain.append(decrypted_block)
    return decrypted_chain

if __name__ == "__main__":
    filename = "blockchain.json"
    with open(filename, "r") as file:
        blockchain = json.load(file)

    decrypted_blockchain = decrypt_blockchain(blockchain)

    print("Decrypted blockchain:")
    print(decrypted_blockchain)
