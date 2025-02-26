
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pywhatkit as wk
import os
import cv2
import pyautogui
import time
import operator
import requests
import threading

# Initialize the speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def handle_response(query):
    if 'falcon' in query:
        return "Yes sir"

    elif "who are you" in query:
        return 'My name is falcon. I can do everything that my creator programmed me to do.'

    elif "who created you" in query:
        return "Praduman Sharma, He Created Me With Python Language, In Visual Studio Code."

    elif 'what is the time' in query:
        return f"Sir, the time is {datetime.datetime.now().strftime('%H:%M:%S')}"

    elif 'what is' in query or 'who is' in query:
        query = query.replace("what is", "").replace("who is", "").strip()
        try:
            results = wikipedia.summary(query, sentences=2)
            return f"According to Wikipedia: {results}"
        except wikipedia.DisambiguationError:
            return "Your query may refer to multiple topics, please be more specific."
        except wikipedia.PageError:
            return "I couldn't find any information on that topic. Please try a different query."
        except requests.exceptions.RequestException:
            return "There was an error connecting to the Wikipedia API. Please check your network connection and try again."

    elif 'open google' in query:
        speak("What do you want to search?")
        qry = takeCommand().lower()
        if qry != "none":
            webbrowser.open(f"https://www.google.com/search?q={qry}")
            try:
                results = wikipedia.summary(qry, sentences=1)
                return results
            except wikipedia.DisambiguationError:
                return "Your query may refer to multiple topics, please be more specific."
            except wikipedia.PageError:
                return "I couldn't find any information on that topic."
            except requests.exceptions.RequestException:
                return "There was an error connecting to the Wikipedia API. Please check your network connection and try again."

    elif 'just open google' in query:
        webbrowser.open('google.com')

    elif 'open youtube' in query:
        speak("What would you like to watch?")
        qrry = takeCommand().lower()
        if qrry != "none":
            wk.playonyt(f"{qrry}")

    elif 'search on youtube' in query:
        query = query.replace("search on youtube", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

    elif 'close browser' in query:
        os.system("taskkill /f /im msedge.exe")

    elif 'close firefox' in query:
        os.system("taskkill /f /im firefox.exe")

    elif 'close chrome' in query:
        os.system("taskkill /f /im chrome.exe")

    elif "open paint" in query:
        npath = r"C:\Users\pradu\AppData\Local\Microsoft\WindowsApps\mspaint.exe"
        try:
            os.startfile(npath)
        except FileNotFoundError:
            return "MS Paint not found at the specified path."

    elif "close paint" in query:
        os.system("taskkill /f /im mspaint.exe")

    elif "open notepad" in query:
        npath = r"C:\Windows\System32\notepad.exe"
        try:
            os.startfile(npath)
        except FileNotFoundError:
            return "Notepad not found at the specified path."

    elif "close notepad" in query:
        os.system("taskkill /f /im notepad.exe")

    elif "open command prompt" in query:
        os.system("start cmd")

    elif "close command prompt" in query:
        os.system("taskkill /f /im cmd.exe")

    elif "open microsoft store" in query:
        os.system("start ms-windows-store:")
        return "Opening Microsoft Store."

    elif "close microsoft store" in query:
        os.system("taskkill /f /im ms-windows-store.exe")
        return "Closing Microsoft Store."

    elif "open camera" in query:
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            cv2.imshow('webcam', img)
            if cv2.waitKey(50) & 0xFF == 27:  # Press 'Esc' to exit
                break
        cap.release()
        cv2.destroyAllWindows()

    elif "close camera" in query:
        cap.release()  # Release the camera
        cv2.destroyAllWindows()  # Close all OpenCV windows
        return "Camera closed successfully."

    elif "take screenshot" in query:
        speak('Tell me a name for the file.')
        name = takeCommand().lower()
        time.sleep(3)
        img = pyautogui.screenshot()
        img.save(f"{name}.png")
        return "Screenshot saved."

    elif "calculate" in query:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            speak("Ready")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            my_string = r.recognize_google(audio)
            def get_operator_fn(op):
                return {
                    '+' : operator.add,
                    '-' : operator.sub,
                    'x' : operator.mul,
                    'divided' : operator.truediv,
                }[op]
            def eval_binary_expr(op1, oper, op2):
                op1, op2 = int(op1), int(op2)
                return get_operator_fn(oper)(op1, op2)
            result = eval_binary_expr(*(my_string.split()))
            return f"Your result is {result}"
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError as e:
            return f"Could not request results; {e}"

    elif "what is my ip address" in query:
        try:
            ipAdd = requests.get('https://api.ipify.org').text
            return f"Your IP address is {ipAdd}"
        except requests.exceptions.RequestException:
            return "There was an error retrieving your IP address. Please check your network connection and try again."

    elif "volume up" in query:
        for _ in range(5):
            pyautogui.press("volumeup")
        return "Volume increased."

    elif "volume down" in query:
        for _ in range(5):
            pyautogui.press("volumedown")
        return "Volume decreased."

    elif "mute" in query or "unmute" in query:
        pyautogui.press("volumemute")
        return "Volume muted/unmuted."

    elif "play" in query:
        song = query.replace("play", "").strip()
        return f"Playing {song}"
        wk.playonyt(song)

    elif 'lock window' in query:
        pyautogui.hotkey('win', 'l')
        return "Device locked."

    elif 'shutdown system' in query:
        os.system('shutdown /s /t 1')
        return "Shutting down the system."

    elif 'restart system' in query:
        os.system('shutdown /r /t 1')
        return "Restarting the system."

    elif "open my documents" in query:
        os.startfile("C:\\Users\\pradu\\Documents")

    elif "close browser" in query:
        os.system("taskkill /f /im msedge.exe")
        os.system("taskkill /f /im firefox.exe")
        os.system("taskkill /f /im chrome.exe")

    elif 'exit' in query:
        return "Goodbye"
    
    else:
        return "Sorry, I didn't understand that."

def start_speech_recognition():
    while True:
        query = takeCommand().lower()
        if query != "none":
            response = handle_response(query)
            speak(response)

def create_gui():
    root = tk.Tk()
    root.title("Falcon AI")
    root.geometry("800x600")

    # Load the downloaded image
    img = Image.open(r"C:\Users\pradu\OneDrive\Documents\Project\Python\Jarvis AI\dead.jpg")
    img = img.resize((800, 600), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    # Create a canvas and add the image
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=photo)

    # Create a frame for content
    frame = ttk.Frame(root, padding="10")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Add a label to the frame
    label = ttk.Label(frame, text="Welcome to Falcon AI", font=("Arial", 24))
    label.pack(pady=20)

    # Add a start button to the frame
    button = ttk.Button(frame, text="Start", command=lambda: threading.Thread(target=start_speech_recognition, daemon=True).start())
    button.pack(pady=10)

    root.mainloop()

create_gui()
