import socket
import os
from cryptography.fernet import Fernet

# Load key
if not os.path.exists("key.key"):
    raise FileNotFoundError("The key file 'key.key' does not exist.")
with open("key.key", "rb") as key_file:
    key = key_file.read()
cipher = Fernet(key)

# Setup client
s = socket.socket()
try:
    s.connect(('localhost', 12345))
    print("📲 Connected to server")

    while True:
        try:
            msg = input("You: ")
            if msg.lower() == "exit":
                print("Exiting chat...")
                break

            encrypted = cipher.encrypt(msg.encode())
            s.send(encrypted)

            encrypted_msg = s.recv(1024)
            decrypted_msg = cipher.decrypt(encrypted_msg).decode()
            print(f"Server: {decrypted_msg}")
        except (socket.error, socket.timeout) as e:
            print(f"Socket error: {e}")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
except ConnectionRefusedError:
    print("Failed to connect to the server. Is it running?")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    s.close()
    print("Connection closed.")