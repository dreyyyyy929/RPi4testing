import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    print("Recording...")
    audio = r.listen(source,phrase_time_limit=20) 
    text = r.recognize_google(audio, language="yue-Hant-hk")
    print(text)