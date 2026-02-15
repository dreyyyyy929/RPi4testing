import ollama

response = ollama.chat(model="qwen2.5:1.5b-instruct", messages=[
    {'role': 'user', 'content': '用廣東話解釋「勇氣」的意思'},
    {'role': 'system', 'content': ''}
])

print("回應:", response['message']['content'])