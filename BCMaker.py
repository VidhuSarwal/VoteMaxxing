import hashlib
import json
from datetime import datetime

def hashCalc(index, timestamp, data, previous_hash):
    return hashlib.sha256(
        str(index).encode('utf-8') +
        str(timestamp).encode('utf-8') +
        str(data).encode('utf-8') +
        str(previous_hash).encode('utf-8')
    ).hexdigest()

def genesisGen():
    return {
        "index": 0,
        "timestamp": str(datetime.now()),
        "data": "Genesis Block",
        "previous_hash": "0",
        "hash": hashCalc(0, datetime.now(), "Genesis Block", "0")
    }

def addBlck(chain, data):
    previous_block = chain[-1]
    index = previous_block["index"] + 1
    timestamp = str(datetime.now())
    previous_hash = previous_block["hash"]
    hash = hashCalc(index, timestamp, data, previous_hash)
    new_block = {
        "index": index,
        "timestamp": timestamp,
        "data": data,
        "previous_hash": previous_hash,
        "hash": hash
    }
    chain.append(new_block)

def svBChain(chain, filename=None):
    if filename is None:
        current_time = datetime.now().strftime("%H-%M--%d-%m-%Y")
        filename = f"blockchain_{current_time}.json"

    try:
        with open(filename, "w") as file:
            json.dump(chain, file, indent=4)
        print(f"Blockchain saved to '{filename}'")
        with open(filename, "r") as file:
            print("Content saved in file:")
            print(file.read())
    except Exception as e:
        print(f"Error saving blockchain: {e}")

if __name__ == "__main__":
    blockchain = [genesisGen()]
    print("Blockchain module initialized.")
