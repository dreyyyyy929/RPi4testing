import threading
import speech_recognition as sr
import ollama
from pynput import keyboard
from gtts import gTTS
from playsound import playsound
import os
import datetime as dt
import json  
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root(name: str = "World"):
    return {"message": f"Hello {name}"}


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
    
def explain_text(text):

    # Generate response from Ollama
    print("Thinking...")
    response = ollama.chat(model="qwen2.5:1.5b-instruct", messages=[
          {'role': 'system', 
             'content': '用粵語口語在四十字解釋以下詞語。如果有多個詞語，請分別簡短解釋每個詞語和整個句子的意思'},

        {'role': 'user',
         'content': f'解釋{text}'}
    ])
    reply = response['message']['content']
    print(f"Lexi 學習助手: {reply}")

    # Save history
    saveHistory(text,reply)

    # Text to Speech
    tts = gTTS(text=reply, lang='yue', slow=False)
    tts.save("output.mp3")
    playsound("output.mp3")

    # Delete temp file
    if os.path.exists("output.mp3"):
        os.remove("output.mp3")


def process_voice_input():
    try:
        with mic as source:
            print("Recording...")
            audio = r.listen(source, timeout=10, phrase_time_limit=20) 
            text = r.recognize_google(audio, language="yue-Hant-hk")
        print(f"用家: {text}")
        explain_text(text)
    except sr.UnknownValueError:
        tts = gTTS(text="唔好意思，Lexi聽唔清楚你的查詢", lang='yue', slow=False)
        tts.save("output.mp3")
        playsound("output.mp3")

def process_camera_input():
    camera_data = {'words': [{'closest_char': '梅', 'line': 0, 'second_closest': '、', 'text': '海棠形、梅花形等等'}]}
    text = camera_data['words']['text']
    print(f"讀取鏡頭數據：{text}")
    explain_text(text)


def on_press(key):
    try:
        if key.char == 's':  
            threading.Thread(target=process_voice_input).start()
        if key.char == 'c':  
            threading.Thread(target=process_camera_input).start()
    except:
        pass

# Main program
print("系統準備就緒")
print("按 's' - 用語音輸入查詢字義")
print("按 'c' - 讀取鏡頭數據查詢字義")

listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()