import requests

BASE_URL = "https://playground.learnqa.ru/ajax/api/compare_query_type"
ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE"]
UNSUPPORTED_METHOD = "HEAD"


def describe_response(resp):
    """Возвращает краткое описание ответа: статус-код, тело, заголовки."""
    return {
        "status_code": resp.status_code,
        "text": resp.text[:200],          # ограничиваем длину для читаемости
        "headers": dict(resp.headers),
    }


def make_request(http_method, params=None, data=None):
    """Универсальная функция для выполнения запроса с указанным HTTP-методом."""
    http_method = http_method.upper()
    if http_method == "GET":
        return requests.get(BASE_URL, params=params)
    elif http_method == "POST":
        return requests.post(BASE_URL, data=data)
    elif http_method == "PUT":
        return requests.put(BASE_URL, data=data)
    elif http_method == "DELETE":
        return requests.delete(BASE_URL, data=data)
    else:
        # Для неподдерживаемых методов используем requests.request
        return requests.request(http_method, BASE_URL, params=params, data=data)


def task_1_no_method():
    """Задача 1: запрос без параметра method."""
    print("=" * 60)
    print("Задача 1: запрос без параметра method")
    for method in ALLOWED_METHODS:
        if method == "GET":
            resp = make_request(method)
        else:
            resp = make_request(method, data={})
        print(f"\n{method} без method → {describe_response(resp)}")


def task_2_unsupported_method():
    """Задача 2: запрос с методом, не входящим в список (HEAD)."""
    print("=" * 60)
    print("Задача 2: запрос с неподдерживаемым методом (HEAD)")
    resp = make_request(UNSUPPORTED_METHOD, params={"method": "HEAD"})
    print(f"HEAD с method=HEAD → {describe_response(resp)}")


def task_3_correct_method():
    """Задача 3: запрос с правильным значением method."""
    print("=" * 60)
    print("Задача 3: запрос с правильным значением method")
    for method in ALLOWED_METHODS:
        if method == "GET":
            resp = make_request(method, params={"method": method})
        else:
            resp = make_request(method, data={"method": method})
        print(f"\n{method} с method={method} → {describe_response(resp)}")


def task_4_all_combinations():
    """Задача 4: перебор всех сочетаний реального метода и method."""
    print("=" * 60)
    print("Задача 4: все сочетания реального HTTP-метода и значения method")
    mismatches = []
    for real_method in ALLOWED_METHODS:
        for param_method in ALLOWED_METHODS:
            if real_method == "GET":
                resp = make_request(real_method, params={"method": param_method})
            else:
                resp = make_request(real_method, data={"method": param_method})

            # Определяем, совпадают ли реальный метод и значение параметра
            is_match = real_method == param_method
            # Предполагаем, что сервер возвращает успех, если текст ответа
            # содержит "success" или "ok" (нужно уточнить по фактическому ответу)
            response_text = resp.text.lower()
            server_thinks_ok = "success" in response_text or "ok" in response_text

            # Фиксируем аномалии:
            # 1) методы не совпадают, но сервер отвечает так, будто всё ок
            # 2) методы совпадают, но сервер считает, что это не так
            if (not is_match and server_thinks_ok) or (is_match and not server_thinks_ok):
                mismatches.append({
                    "real_method": real_method,
                    "param_method": param_method,
                    "status": resp.status_code,
                    "response": resp.text[:150],
                })

            print(f"{real_method} / method={param_method} → {resp.status_code}, "
                  f"текст: {resp.text[:80]}...")

    print("\n--- Найденные аномалии ---")
    if mismatches:
        for m in mismatches:
            print(m)
    else:
        print("Аномалий не обнаружено (при текущем критерии успеха).")


if __name__ == "__main__":
    task_1_no_method()
    task_2_unsupported_method()
    task_3_correct_method()
    task_4_all_combinations()