import threading
import speech_recognition as sr
import ollama
from gtts import gTTS
from playsound import playsound
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

def save_history(prompt, response):
    history = []
    if os.path.exists('history.txt'):
        try:
            with open('history.txt', 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    history = json.loads(content)
        except:
            history = []
    
    history.append({
        "timestamp": dt.datetime.now().isoformat(),
        "prompt": prompt,
        "response": response
    })
    
    with open('history.txt', 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def explain(cam, voice):
    #Ollama
    text = f"鏡頭檢測到的詞語: {cam}\n用家語音補充: {voice}\n請根據以上資訊解釋"
    response = ollama.chat(model="qwen2.5:1.5b-instruct", messages=[
        {'role': 'system', 'content': '用粵語口語在四十字解釋以下詞語。如果有多個詞語，請分別簡短解釋每個詞語和整個句子的意思'},
        {'role': 'user', 'content': f'解釋{text}'}
    ])
    reply = response['message']['content']
    print(f"Lexi: {reply}")

    #save history
    save_history(text, reply)

    #play explanation
    tts = gTTS(text=reply, lang='yue', slow=False)
    tts.save("output.mp3")
    playsound("output.mp3")
    if os.path.exists("output.mp3"):
        os.remove("output.mp3")

def record_voice():
    global voice_text
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Recording voice...")
            audio = r.listen(source, timeout=15, phrase_time_limit=20)
            voice_text = r.recognize_google(audio, language="yue-Hant-hk")
        print(f"User: {voice_text}")
    except:
        voice_text = None
    finally:
        voice_done.set()

@app.post("/button_press")
async def button_press(request: Request):
    global voice_text
    voice_text = None
    voice_done.clear()
    threading.Thread(target=record_voice).start()
    button_pressed.set()
    return {"status": "button_pressed"}

@app.post("/camera_data")
async def receive_camera_data(request: Request):
    request_data = await request.json()
    cam_data = request_data['words'][-1]['closest_char']
    camera_queue.put(cam_data)
    return {"status": "camera_data_received"}

def process_explanation():
    global voice_text
    voice_done.wait()
    
    current_voice_text = voice_text if voice_text is not None else "鏡頭偵測到嘅字係咩意思"
    
    try:
        cam_data = camera_queue.get(timeout=10)
    except:
        cam_data = "未檢測到詞語"
    
    explain(cam_data, current_voice_text)

def main_workflow():
    print("Server starting at http://0.0.0.0:8000")
    
    while True:
        button_pressed.wait()
        button_pressed.clear()
        threading.Thread(target=process_explanation).start()

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

main_workflow()