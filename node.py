from fastapi import FastAPI
from pydantic import BaseModel
from blockchain import Blockchain
import config
import uvicorn
import requests

app = FastAPI()
blockchain = Blockchain()

# Daftar alamat node peer (tambahkan sesuai node yang kamu punya)
PEERS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
]

class Transaction(BaseModel):
    sender: str
    recipient: str
    amount: float

class ChainData(BaseModel):
    chain: list

@app.post("/add_transaction")
def add_transaction(tx: Transaction):
    blockchain.add_block(tx.sender, tx.recipient, tx.amount)
    broadcast_chain()  # Broadcast ke semua node peer
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
    # Cek apakah chain baru lebih panjang dan valid
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
    for peer in PEERS:
        try:
            requests.post(f"{peer}/receive_chain", json={"chain": chain})
        except Exception as e:
            print(f"Gagal broadcast ke {peer}: {e}")

if __name__ == "__main__":
    uvicorn.run("node:app", host="127.0.0.1", port=config.PORT, reload=True)
