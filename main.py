import requests
import hashlib

API_URL = "http://127.0.0.1:8000"  # Jangan diubah kalau pakai uvicorn default

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
        print("1. Tambah Transaksi")
        print("2. Lihat Semua Block")
        print("3. Keluar")
        choice = input("Pilih menu: ")

        if choice == '1':
            sender = input("Nama Pengirim: ")
            recipient = input("Nama Penerima: ")
            amount = float(input("Jumlah: "))

            hashed_sender = hash_user(sender)
            payload = {
                "sender": hashed_sender,
                "recipient": recipient,
                "amount": amount
            }

            response = requests.post(f"{API_URL}/add_block", json=payload)
            print(response.json())



        elif choice == '2':
            response = requests.get(f"{API_URL}/chain")
            data = response.json()
            blocks = data["chain"]

            for block in blocks:
                print_block(block)

        elif choice == '3':
            print("Sampai jumpa, Onii-chan~! >///<")
            break

        else:
            print("Pilihan tidak valid. Coba lagi.")

if __name__ == "__main__":
    main()
