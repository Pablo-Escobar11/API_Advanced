import pprint
import time
from json import loads
from datetime import datetime

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mail_hog_api import MailhogApi


def test_v1_account():
    # Подготовка данных
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mail_hog_api = MailhogApi(host='http://5.63.153.31:5025')

    current_time = datetime.now()
    formatted_time = current_time.strftime("%m_%d_%H_%M_%S")
    login = f'pasha_{formatted_time}'
    email = f'{login}@mail.ru'
    password = 'Qwerty123'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    time.sleep(1)
    # Регистрация пользвателя
    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f"Пользователь не был создан, {response.json()}"

    # Получение письма
    response = mail_hog_api.get_api_v2_messages()
    assert response.status_code == 200, f"Письма не были получены, {response.json()}"

    # Получение токена
    register_token = get_activation_token_by_login(login=login, response=response)
    assert register_token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=register_token)
    assert response.status_code == 200, f'Пользователь не активен {response.json()}'

    # Логин пользвателя в систему
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, f'Пользователь не авторизован {response.json()}'

    # Смена почты
    new_email = f'new{email}'
    json_data = {
        "login": login,
        "password": password,
        "email": new_email
    }
    response = account_api.put_v1_account_email(json_data=json_data)
    assert response.status_code == 200, f'Запрос на сброс почты не отправлен, {response.json()}'

    # Логин пользвателя в систему после смены почты
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 403, f'Пользователь авторизован {response.json()}'

    # Получение письма
    response = mail_hog_api.get_api_v2_messages()
    assert response.status_code == 200, f"Письма не были получены, {response.json()}"

    # Получение токена для почты
    email_token = get_reset_token_for_email(response=response, login=login, email=new_email)

    # Потверждение новой почты
    response = account_api.put_v1_account_token(token=email_token)
    assert response.status_code == 200, f"Почта не иизменена, {response.json()}"

    # Логин пользвателя в систему
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, f'Пользователь не авторизован {response.json()}'


def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token


def get_auth_token_by_login(response):
    if 'X-Dm-Auth-Token' in response.headers:
        return response.headers['X-Dm-Auth-Token']
    else:
        print('There is no token in headers')


def get_reset_token_for_email(login, response, email):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login and email == item['Content']['Headers']['To'][0]:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token
