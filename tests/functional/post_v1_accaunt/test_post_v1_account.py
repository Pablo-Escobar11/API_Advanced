import time
from json import loads
from datetime import datetime

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mail_hog_api import MailhogApi
import structlog
from rest_client.configuration import Configuration as MailHogConfiguration
from rest_client.configuration import Configuration as DmApiConfiguration
structlog.configure(
    processors=[structlog.processors.JSONRenderer(indent=4,
                                                  ensure_ascii=True,
                                                  # sort_keys=True
                                                  )
                ]
)


def test_v1_account():
    mail_configuration = MailHogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    # Регистрация пользователя!!!!!!!!!!!!!!!!!!!!!!!!!
    account_api = AccountApi(configuration=dm_api_configuration)
    login_api = LoginApi(configuration=dm_api_configuration)
    mail_hog_api = MailhogApi(configuration=mail_configuration)

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
    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f"Пользователь не был создан, {response.json()}"

    # Получить письма !!!!!!!!!!!!!!!!!!!!!!!!

    response = mail_hog_api.get_api_v2_messages()
    assert response.status_code == 200, f"Письма не были получены, {response.json()}"

    # Получить токен !!!!!!!!!!!
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, f'Пользователь не активен {response.json()}'

    # Авторизация !!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, f'Пользователь не авторизован {response.json()}'

    # Получение данных о пользователе

    aut_token = get_auth_token_by_login(response)
    response = account_api.get_v1_account(auth_token=aut_token)
    assert response.status_code == 200, f"Данные о пользователи не были получены {response.json()}"

    # Сброс пароля пользователя
    json_data = {
        'login': login,
        'email': email
    }
    response = account_api.post_v1_account_password(json_data=json_data)
    assert response.status_code == 200

    response = mail_hog_api.get_api_v2_messages()
    reset_token = get_reset_token_by_login(login=login, response=response)

    # Сменапароля пользователя
    json_data = {
        "login": login,
        "token": reset_token,
        "oldPassword": password,
        "newPassword": "Qwert123"
    }
    response = account_api.put_v1_account_password(json_data=json_data)
    assert response.status_code == 200, f"Пароль не был изменен, {response.json()}"

    # Выход
    response = login_api.delete_v1_account_login(auth_token=aut_token)
    assert response.status_code == 204, f"Выход не был выполнен, {response.json()}"


def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token


def get_reset_token_by_login(login, response):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login and user_data.get('ConfirmationLinkUri'):
            token = user_data['ConfirmationLinkUri'].split('/')[-1]
        return token


def get_auth_token_by_login(response):
    if 'X-Dm-Auth-Token' in response.headers:
        return response.headers['X-Dm-Auth-Token']
    else:
        print('There is no token in headers')
