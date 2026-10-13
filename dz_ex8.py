import requests
import time

base_url = "https://playground.learnqa.ru/ajax/api/longtime_job"

response_without_token = requests.get(base_url)
response_without_token_json = response_without_token.json()
token = response_without_token_json["token"]
timer = response_without_token_json["seconds"]
print('Наш токен -', token)
print('Ждать нужно',timer, 'секунд')
response_with_token = requests.get(base_url, params={"token":token})
response_with_token_json = response_with_token.json()
print('Статус задачи - ', response_with_token_json['status'])
assert response_with_token_json['status'] == 'Job is NOT ready'
time.sleep(timer)
response_with_token_after = requests.get(base_url, params={"token":token})
response_with_token_json_after = response_with_token_after.json()
print('Ожидание завершено')
assert response_with_token_json_after['status'] == 'Job is ready'
print('Статус задачи - ', response_with_token_json_after['status'])
assert "result" in response_with_token_json_after
print('Результат - ', response_with_token_json_after['result'])