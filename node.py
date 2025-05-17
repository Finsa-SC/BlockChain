from fastapi import FastAPI, Request
from pydantic import BaseModel
from blockchain import Blockchain
import config
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
    blocks = blockchain.get_all_blocks()
    chain_data = [block.to_dict() for block in blocks]
    return {
        "length": len(chain_data),
        "chain": chain_data
    }



@app.get("/ping")
def ping():
    return {"status": "alive"}

if __name__ == "__main__":
    uvicorn.run("node:app", host="127.0.0.1", port=config.PORT, reload=True)
