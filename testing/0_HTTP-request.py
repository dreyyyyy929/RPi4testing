import requests
url='https://trusted-pony-deadly.ngrok-free.app/predict'
results = requests.get(url)
print(results.text)