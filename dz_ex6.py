import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
response_history = response.history
for i in range (len(response_history)):
    print (response_history[i].url)