import pprint

import requests
from json import loads
from datetime import datetime


def test_v1_account():
    # Регистрация пользователя!!!!!!!!!!!!!!!!!!!!!!!!!
    current_time = datetime.now()
    formatted_time = current_time.strftime("%m_%d_%H_%M_%S")
    login = f'pasha_{formatted_time}'
    email = f'{login}@mail.ru'
    password = 'Qwerty1'
    print(login)
    print(email)

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    assert response.status_code == 201, f"Пользователь не был создан, {response.json()}"

    # Получить письма !!!!!!!!!!!!!!!!!!!!!!!!

    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    assert response.status_code == 200, f"Письма не были получены, {response.json()}"

    # Получить токен !!!!!!!!!!!
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    headers = {
        'accept': 'text/plain',
    }

    response = requests.put(f'http://5.63.153.31:5051/v1/account/{token}', headers=headers)
    assert response.status_code == 200, f'Пользователь не активен {response.json()}'

    # Авторизация !!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    assert response.status_code == 200, f'Пользователь не авторизован {response.json()}'
