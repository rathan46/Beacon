import sqlite3
import random

print("hello user ")

con = sqlite3.connect('beacon.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS auth (uid TEXT, passphrase TEXT)''')
con.commit()
con.close()

def generate_uid():
    con = sqlite3.connect('beacon.db')
    cur = con.cursor()
    while True:
        uid = str(random.randint(911111111111, 999999999999))
        cur.execute('SELECT uid FROM auth WHERE uid = ?', (uid,))
        if not cur.fetchone():
            break
    passphrase = generate_passphrase()
    cur.execute('INSERT INTO auth (uid, passphrase) VALUES (?, ?)', (uid, passphrase))
    print(f"Your UID is: {uid}")
    print(f"Your passphrase is: {passphrase}")
    con.commit()
    con.close()

def generate_passphrase():
    values = [
         'and', 'any', 'ask', 'bad', 'bag', 'bit', 'box', 'bus', 'car', 'cat',
         'cow', 'cry', 'day', 'dog', 'dry', 'ear', 'egg', 'eye', 'fan', 'fat',
         'fly', 'fun', 'god', 'gun', 'hat', 'ice', 'jam', 'job', 'joy', 'key',
         'law', 'lip', 'mad', 'man', 'map', 'net', 'not', 'off', 'oil', 'one',
         'out', 'own', 'pay', 'pen', 'pie', 'pig', 'pop', 'pot', 'put', 'ran',
         'red', 'row', 'run', 'sad', 'say', 'see', 'set', 'she', 'shy', 'sit',
         'six', 'sky', 'son', 'sun', 'tap', 'the', 'tie', 'tip', 'top', 'toy',
         'try', 'tub', 'two', 'use', 'war', 'was', 'way', 'web', 'win', 'yes',
         'yet', 'you']
    passphrase = []
    for i in range(16):
        passphrase.append(random.choice(values))
    return ','.join(passphrase)

def delete(uid):
    con = sqlite3.connect('beacon.db')
    cur = con.cursor()
    cur.execute('DELETE FROM auth WHERE uid = ?', (uid,))
    con.commit()
    con.close()
    
def show_data():
    con = sqlite3.connect('beacon.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM auth')
    rows = cur.fetchall()
    for row in rows:
        print(row)
    con.close()

print("menu")
print("1. Generate UID")
print("2. Show all UIDs")
print("3. Delete UID")
print("4. Exit")
while True:
    choice = input("Enter your choice: ")
    if choice == '1':
        generate_uid()
    elif choice == '2':
        show_data()
    elif choice == '3':
        uid = input("Enter the UID to delete: ")
        delete(uid)
        print(f"UID {uid} deleted.")
    elif choice == '4':
        break
    else:
        print("Invalid choice. Please try again.")
        
# This code is for a user registrar that generates unique UIDs and passphrases, stores them in a SQLite database, and allows for deletion of UIDs. It also provides a menu for user interaction.
# The UID is a random 12-digit number, and the passphrase is a comma-separated string of 16 random words from a predefined list. The code uses SQLite for database operations and provides functions to generate UIDs, generate passphrases, delete UIDs, and show all UIDs in the database.
# The user can choose to generate a new UID, view all UIDs, delete a specific UID, or exit the program through a simple text-based menu interface. The code ensures that the UID is unique by checking against existing entries in the database before inserting a new one.
# The passphrase generation uses a predefined list of words to create a random passphrase, which is also stored in the database along with the UID. The code handles database connections and queries using the sqlite3 module, ensuring that resources are properly managed and closed after use.
# Overall, this code provides a basic user registrar system with UID and passphrase generation, storage, and management functionalities.