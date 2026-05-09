import socket
import os


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
server.listen(1)

print("Server waiting for connection...")

def capture_msg(conn):
    try:
        data = conn.recv(1024).decode()
        if data:
            print(f"\nClient: {data}")
            return data
    except socket.timeout:
        return None
    except:
        raise   # 🔥 important (disconnect ধরার জন্য)

while True:   # 🔥 main loop add
    conn, addr = server.accept()
    print(f"Connected with {addr}")

    conn.settimeout(0.10)

    try:
        while True:
            msg = input("You (Server): ")
            conn.send(msg.encode())

            if msg.lower() == "exit":
                break

            if msg.lower() == "clear":
                os.system("cls")
                os.system("clear")

            if msg.lower() == "banner":
                print(banner)

            while True:
                data = capture_msg(conn)
                if data is None:
                    continue
                else:
                    break

    except:
        print("Client disconnected. Waiting again...\n")
        conn.close()
        continue   # 🔥 আবার accept এ যাবে

conn.close()
server.close()