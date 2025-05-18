from fastapi import FastAPI
from pydantic import BaseModel
from blockchain import Blockchain
import config
import uvicorn
import requests

app = FastAPI()
blockchain = Blockchain()

peers = config.PEERS


class Transaction(BaseModel):
    sender: str
    recipient: str
    amount: float

class ChainData(BaseModel):
    chain: list

@app.post("/add_transaction")
def add_transaction(tx: Transaction):
    blockchain.add_block(tx.sender, tx.recipient, tx.amount)
    broadcast_chain()
    return {"message": "Transaction added"}

@app.get("/chain")
def get_chain():
    blocks = blockchain.get_all_blocks()
    chain_data = [block.to_dict() for block in blocks]
    return {
        "length": len(chain_data),
        "chain": chain_data
    }

@app.post("/receive_chain")
def receive_chain(data: ChainData):
    incoming_chain = data.chain
    current_chain = blockchain.get_all_blocks()
    if len(incoming_chain) > len(current_chain) and blockchain.is_valid_chain(incoming_chain):
        blockchain.replace_chain(incoming_chain)
        return {"message": "Chain replaced"}
    else:
        return {"message": "Received chain is not longer or not valid"}

@app.get("/ping")
def ping():
    return {"status": "alive"}

def broadcast_chain():
    chain = [block.to_dict() for block in blockchain.get_all_blocks()]
    for peer in peers   :
        try:
            requests.post(f"{peer}/receive_chain", json={"chain": chain})
        except Exception as e:
            print(f"Failed broadcast to {peer}: {e}")

@app.get("/sync_chain")
def sync_chain():
    global blockchain
    longest_chain = None
    max_length = len(blockchain.get_all_blocks())

    for peer in peers:
        if peer == f"http://127.0.0.1:{config.PORT}":
            continue

        try:
            res = requests.get(f"{peer}/chain")
            if res.status_code == 200:
                data = res.json()
                length = data["length"]
                chain = data["chain"]

                if length > max_length and blockchain.is_valid_chain(chain):
                    max_length = length
                    longest_chain = chain
        except:
            continue

    if longest_chain:
        blockchain.replace_chain(longest_chain)
        return {"message": "Chain is replaced by a longer version"}
    else:
        return {"message": "Already used the longest chain"}

if __name__ == "__main__":
    uvicorn.run("node:app", host="127.0.0.1", port=config.PORT, reload=True)
