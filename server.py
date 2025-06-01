import socket
from cryptography.fernet import Fernet

# Load key
key = open("key.key", "rb").read()
cipher = Fernet(key)

# Setup server
s = socket.socket()
s.bind(('localhost', 12345))
s.listen(1)

print("🔒 Server ready, waiting for client...")
conn, addr = s.accept()
print(f"✅ Connected with {addr}")

while True:
    encrypted_msg = conn.recv(1024)
    decrypted_msg = cipher.decrypt(encrypted_msg).decode()
    print(f"Client: {decrypted_msg}")

    msg = input("You: ")
    encrypted = cipher.encrypt(msg.encode())
    conn.send(encrypted)