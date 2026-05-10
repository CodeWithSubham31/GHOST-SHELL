import socket
import threading
import os
import time

banner = """
 ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗███████╗██╗  ██╗███████╗██╗     ██╗     
██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝██╔════╝██║  ██║██╔════╝██║     ██║     
██║  ███╗███████║██║   ██║███████╗   ██║   ███████╗███████║█████╗  ██║     ██║     
██║   ██║██╔══██║██║   ██║╚════██║   ██║   ╚════██║██╔══██║██╔══╝  ██║     ██║     
╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ███████║██║  ██║███████╗███████╗███████╗
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝

            GhostShell v1.0
"""

print(banner)

HOST = '0.0.0.0'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

clients = []

print("Server waiting for connection...")


# 🔥 receive thread
def receive_thread(conn, addr):
    while True:
        try:
            data = conn.recv(1024).decode()
            if data:
                print(f"\nClient [{addr[0]}]: {data}")
        except:
            print(f"\nClient {addr[0]} disconnected!\n")
            conn.close()
            if (conn, addr) in clients:
                clients.remove((conn, addr))
            break


# 🔥 accept thread
def accept_clients():
    while True:
        conn, addr = server.accept()
        clients.append((conn, addr))
        print(f"\nConnected with {addr[0]}")


threading.Thread(target=accept_clients, daemon=True).start()


# 🔥 MAIN LOOP (ALWAYS SELECT)
while True:

    if len(clients) == 0:
        print("Waiting for client connection...")
        time.sleep(2)
        continue

    # 🔥 ALWAYS SHOW LIST
    print("\nConnected Clients:")
    for i, (c, a) in enumerate(clients, start=1):
        print(f"{i}. {a[0]}")

    print("0. All Clients")

    try:
        choice = int(input("Select client: "))
    except:
        continue

    if choice == 0:
        selected = clients
    elif 1 <= choice <= len(clients):
        selected = [clients[choice - 1]]
    else:
        continue

    # 🔥 start receive threads for selected (if not already running)
    for conn, addr in selected:
        threading.Thread(target=receive_thread, args=(conn, addr), daemon=True).start()

    # 🔥 SEND LOOP
    while True:
        msg = input("You (Server): ")

        if msg.lower() == "exit":
            break

        if msg.lower() == "back":
            print("Back to client list...\n")
            break

        if msg.lower() == "clear":
            os.system("cls")
            os.system("clear")
            continue

        if msg.lower() == "banner":
            print(banner)
            continue

        for conn, addr in selected:
            try:
                conn.send(msg.encode())
            except:
                print(f"Failed to send to {addr[0]}")