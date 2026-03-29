import threading
import speech_recognition as sr
import ollama
from gtts import gTTS
import pygame
import os
import datetime as dt
import json  
from fastapi import FastAPI, Request
import uvicorn
import queue

camera_queue = queue.Queue()
button_pressed = threading.Event()
voice_done = threading.Event()
voice_text = None

r = sr.Recognizer()
mic = sr.Microphone()
app = FastAPI()

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

def explain_text(cam, voice):
    text = f"鏡頭檢測到的詞語: {cam}\n用家語音補充: {voice}\n請根據以上資訊解釋"
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
    saveHistory(text, reply)

    # Text to Speech
    tts = gTTS(text=reply, lang='yue', slow=False)
    tts.save("output.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)

    # Delete temp file
    if os.path.exists("output.mp3"):
        os.remove("output.mp3")

def process_voice_input():
    global voice_text
    try:
        with mic as source:
            print("Recording...")
            audio = r.listen(source, timeout=10, phrase_time_limit=20) 
            voice_text = r.recognize_google(audio, language="yue-Hant-hk")
        print(f"用家: {voice_text}")
    except:
        voice_text = None
    finally:
        voice_done.set()

@app.post("/button_press")
async def button_press():
    global voice_text
    voice_text = None
    voice_done.clear()
    threading.Thread(target=process_voice_input).start()
    button_pressed.set()
    return {"status": "button_pressed"}

@app.post("/camera_data")
async def process_camera_input(request: Request):
    request_data = await request.json()
    cam_data = request_data['words'][-1]['closest_char']
    camera_queue.put(cam_data)
    return {"status": "camera_data_received"}

def process_explanation():
    global voice_text
    voice_done.wait()
    
    if voice_text is not None:
        current_voice_text = voice_text 
    else:
        current_voice_text = "鏡頭偵測到嘅字係咩意思"
    
    try:
        cam_data = camera_queue.get(timeout=10)
    except:
        cam_data = "未檢測到詞語"
    
    explain_text(cam_data, current_voice_text)
    

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

# Main program

print("系統準備就緒")
print("按 's' - 用語音輸入查詢字義")
print("FastAPI server starting at http://0.0.0.0:8000")

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

while True:
    button_pressed.wait()
    button_pressed.clear()
    threading.Thread(target=process_explanation).start()