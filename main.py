import threading
import speech_recognition as sr
import ollama
from pynput import keyboard
from gtts import gTTS
from playsound import playsound
import os
import datetime as dt
import json  

r = sr.Recognizer()
mic = sr.Microphone()

def saveHistory(prompts, response):
    new_entry = {
        "timestamp": dt.datetime.now().isoformat(),
        "prompt": prompts,
        "response": response
    }

    history = []
    if os.path.exists('history.txt'):
        try:
            with open('history.txt', 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:  # If file is not empty
                    history = json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError):
            history = []
    
    history.append(new_entry)
    
    with open('history.txt', 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
        
    print(f"History saved at {new_entry['timestamp']}")
    
def run_chat_cycle():

    # 1 Record
   with mic as source:
    print("Recording...")
    audio = r.listen(source, timeout=10, phrase_time_limit=20) 
    text = r.recognize_google(audio, language="yue-Hant-hk")
    print(f"用家: {text}")

    if not text: return

    # 2 Ollama
    print("Thinking...")
    response = ollama.chat(model="qwen2.5:1.5b-instruct", messages=[
          {'role': 'system', 
             'content': '10字以內'},

        {'role': 'user',
         'content': f'解釋{text}'}
    ])
    reply = response['message']['content']
    print(f"Lexi 學習助手: {reply}")

    saveHistory(text,reply)
    # 3 Text to Speech
    tts = gTTS(text=reply, lang='yue', slow=False)
    tts.save("output.mp3")
    playsound("output.mp3")

    # 4 Delete temp file
    if os.path.exists("output.mp3"):
        os.remove("output.mp3")

def on_press(key):
    try:
        if key.char == 's':  
            threading.Thread(target=run_chat_cycle).start()
    except:
        pass

print("系統準備就緒. 輸入 's' 開始通話.")

listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()