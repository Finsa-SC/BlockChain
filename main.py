import requests
import hashlib

API_URL = "http://127.0.0.1:8000"

def hash_user(name):
    return hashlib.sha256(name.encode()).hexdigest()

def print_block(block):
    print("┌────────────────────────────┐")
    print(f"│ Block #{block['index']}")
    print("├────────────────────────────┤")
    print(f"│ Timestamp     : {block['timestamp']}")
    print(f"│ Sender (Hash) : {block['sender']}")
    print(f"│ Recipient     : {block['recipient']}")
    print(f"│ Amount        : {block['amount']}")
    print(f"│ Previous Hash : {block['previous_hash']}")
    print(f"│ Nonce         : {block['nonce']}")
    print(f"│ Hash          : {block['hash']}")
    print("└────────────────────────────┘\n")

def main():
    while True:
        print("\n==============================")
        print("      ⛓️ BLOCKCHAIN MENU")
        print("==============================")
        print("1. Add Transaction")
        print("2. View All Blocks")
        print("3. Exit")
        choice = input("Choose menu: ")

        if choice == '1':
            sender = input("Sender Name: ")
            recipient = input("recipient name: ")
            amount = float(input("Amount: "))

            hashed_sender = hash_user(sender)
            payload = {
                "sender": hashed_sender,
                "recipient": recipient,
                "amount": amount
            }

            response = requests.post(f"{API_URL}/add_transaction", json=payload)
            print(response.json())

            sync_res = requests.get(f"{API_URL}/sync_chain")
            print("Sync result:", sync_res.json())

        elif choice == '2':
            response = requests.get(f"{API_URL}/chain")
            data = response.json()
            blocks = data["chain"]

            for block in blocks:
                print_block(block)

        elif choice == '3':
            print("Good Bye")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
