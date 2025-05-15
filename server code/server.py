import socket
import threading
import sqlite3
import hashlib
import time
import json
import os
import random

global  blockchain
global ghash

#BlockChain class to store user events

class Block:
    def __init__(self, index, timestamp, uid, event, previous_hash, nonce=0, hash=None):
        self.index = index
        self.timestamp = timestamp
        self.uid = uid
        self.event = event
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = hash or self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "uid": self.uid,
            "event": self.event,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return self.secure_hash(block_string)  # assuming rhash returns a hex string

    def secure_hash(self, data):
        return hashlib.sha256(data).hexdigest()
    

    
class Blockchain:
    def __init__(self, filename="blockchain.json"):
        self.filename = filename
        self.chain = []
        self.load_chain()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), "GENESIS", "Blockchain Initialized", "0")
        self.chain.append(genesis_block)
        self.save_chain()

    def add_block(self, uid, event):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), time.time(), ghash.rhash(uid), ghash.rhash(event), previous_block.hash)
        new_block = self.proof_of_work(new_block)
        self.chain.append(new_block)
        self.save_chain()

    def proof_of_work(self, block, difficulty=2):
        while not block.hash.startswith("0" * difficulty):
            block.nonce += 1
            block.hash = block.compute_hash()
        return block

    def save_chain(self):
        with open(self.filename, "w") as file:
            json.dump([block.__dict__ for block in self.chain], file, indent=4)

    def load_chain(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                data = json.load(file)
                self.chain = [Block(**block) for block in data]
        else:
            self.create_genesis_block()

    def get_chain(self):
        return [block.__dict__ for block in self.chain]

blockchain = Blockchain()



# Hashing format to handle hashing

class hasher:
    def __init__(self):
        self.capital = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P','Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '~',
            '!', '@', '#', '$', '%','^', '&', '*', '(', ')', '_', '+', '{', '}', ':', '"', '<', '>', '?', '|']

        self.small = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p','q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '`', 
            '-', '=', '[', ']', '/','.', ',', ';','0','1','2','3','4','5','6','7','8','9']

    def hash(self, text): 
        binary_representation = ''.join(format(ord(char), '08b') for char in text)
        hashed_representation = []
        for bit in binary_representation:
            if bit == '1':
                hashed_representation.append(random.choice(self.capital))
            else:
                hashed_representation.append(random.choice(self.small))
        hashed_text = ''.join(hashed_representation)
        #return hashed_text
        return hashed_text

    def rhash(self, input_hash): 
        binary = ''.join('1' if char in self.capital else '0' for char in input_hash)
        reversed_text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
        #return reversed_text
        return reversed_text
ghash = hasher()


# main server code

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 54321))  # Replace with your IP and port
server.listen()

# Dictionaries to keep track of clients and their nicknames
clients = {}
uids = {}

def broadcast(message):
    for client in clients.values():
        try:
            client.send(message)
        except:
            continue

def recieve(client):
    uid = None  # Declare uid here for use in exception block
    while True:
        try:
            conn = sqlite3.connect('beacon.db')
            cur = conn.cursor()
            # Receiving messages from the client
            message = client.recv(1024).decode()
            if "~" in message:
                uid = message.split("~")[0]
                passphrase = message.split("~")[1]
                rcvip = message.split("~")[2]
                cur.execute('SELECT uid, passphrase FROM auth WHERE uid = ?', (uid,))
                row = cur.fetchone()
                if row and row[1] == passphrase:
                    client.send("AUTH_SUCCESS".encode())
                    print("Authentication successful for UID:", uid)
                    #blockchain = Blockchain()
                    user = uid
                    event = "Authentication successful"
                    blockchain.add_block(ghash.hash(user), ghash.hash(event))
                    #bstart(hash(uid), hash("Authentication successful"))
                    clients[uid] = rcvip
                    uids[rcvip] = uid
                else:
                    client.send("AUTH_FAIL".encode())
                    print("Authentication failed for UID:", uid)
                    user = uid
                    event = "Authentication failed"
                    blockchain.add_block(ghash.hash(user), ghash.hash(event))
                    #bstart(hash(uid), hash("Authentication failed"))
                conn.commit()
                conn.close()
            elif "$" in message:
                search_uid = message.split("$")[1]
                print(message)
                if search_uid in clients:
                    # Here we send the IP address of the target client
                    ip = clients[search_uid]
                    print((ip))
                    client.send(ip.encode())
                    print(f"IP address of {search_uid} sent to {uids[client]}")
                    user = uids[client]
                    event = "IP address of" + search_uid + "sent"
                    blockchain.add_block(ghash.hash(user), ghash.hash(event))
                    #bstart(hash(uids[client]), hash(f"IP address of {search_uid} sent"))
                else:
                    client.send("FAIL".encode())
                    print(f"Client {search_uid} not found")
                    user = uids[client]
                    event = "Client" + search_uid + "not found"
                    blockchain.add_block(ghash.hash(user), ghash.hash(event))
                    #bstart(hash(uids[client]), hash(f"Client {search_uid} not found"))
        except Exception as e:
            if client in uids:
                uid = uids[client]
                del clients[uid]
                del uids[client]
            client.close()
            print(f"Connection closed for UID: {uid}")
            user = uid
            event = "Connection closed"
            blockchain.add_block(ghash.hash(user), ghash.hash(event))
            #bstart(hash(uid), hash("Connection closed"))
            break

# Function to receive and set up clients
def handle():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        #blockchain = Blockchain()
        user = "server"
        event = f"Connected with {address}"
        blockchain.add_block(ghash.hash(user), ghash.hash(event))
        #bstart(hash("Server"), hash(f"Connected with {address}"))

        # Start handling thread for the client
        thread = threading.Thread(target=recieve, args=(client,))
        thread.start()

print("Server is listening...")
handle()


# Note: The above code is a simplified version and may require additional error handling and security measures for production use.
# The hashing and blockchain functionality is basic and should be improved for real-world applications.
# The database connection should also be managed more robustly, especially in a multi-threaded environment.
# The server is currently set to listen on localhost and port 54321, which should be changed for actual deployment.
# The code assumes that the ghash module is in the same directory and contains the hash and rhash functions.
