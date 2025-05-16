# node.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from blockchain import Blockchain
from block import Block
import uvicorn

app = FastAPI()
blockchain = Blockchain()

class Transaction(BaseModel):
    sender: str
    recipient: str
    amount: float

@app.post("/add_transaction")
def add_transaction(tx: Transaction):
    blockchain.add_block(tx.sender, tx.recipient, tx.amount)
    return {"message": "Transaction added"}

@app.get("/chain")
def get_chain():
    return {"length": len(blockchain.chain), "chain": [block.__dict__ for block in blockchain.chain]}

@app.get("/ping")
def ping():
    return {"status": "alive"}

if __name__ == "__main__":
    uvicorn.run("node:app", host="0.0.0.0", port=8000, reload=True)
