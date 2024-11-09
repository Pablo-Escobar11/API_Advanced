import time
from json import loads
from datetime import datetime

from dm_api_account.apis.account_api import AccountApi
from api_mailhog.apis.mail_hog_api import MailhogApi


def test_put_v1_account_token():
    # Подготовка данных
    account_api = AccountApi(host='http://5.63.153.31:5051')
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
    # Регистрация пользоателя

    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f"Пользователь не был создан, {response.json()}"

    # Получения письма

    response = mail_hog_api.get_api_v2_messages()
    assert response.status_code == 200, f"Письма не были получены, {response.json()}"

    # Получить токен !!!!!!!!!!!
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, f'Пользователь не активен {response.json()}'


def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token
