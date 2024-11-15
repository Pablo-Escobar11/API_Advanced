import time
from json import loads
from datetime import datetime
import structlog

from helpers.account_helper import AccountHelper
from rest_client.configuration import Configuration as MailHogConfiguration
from rest_client.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogapi

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
    account = DMApiAccount(configuration=dm_api_configuration)
    mail_hog = MailHogapi(configuration=mail_configuration)

    account_helper = AccountHelper(dm_account_api=account, mail_hog=mail_hog)

    current_time = datetime.now()
    formatted_time = current_time.strftime("%m_%d_%H_%M_%S")
    login = f'pasha_{formatted_time}'
    email = f'{login}@mail.ru'
    password = 'Qwerty123'
    new_password = 'Qwert4321'
    time.sleep(1)

    account_helper.register_new_user(login=login, password=password, email=email)

    response = account_helper.user_login(login=login, password=password)
    auth_token = get_auth_token_by_response(response=response)

    # Получение данных о пользователе

    account_helper.get_user_info(auth_token=auth_token)

    # Сброс и смена пароля пользователя
    account_helper.reset_and_change_password(email=email, new_password=new_password, old_password=password, login=login)

    # Вход с новым паролем

    response = account_helper.user_login(login=login, password=new_password)
    assert response.status_code == 200, f'Пользователь не авторизован {response.json()}'


    # Выход
    account_helper.logout_from_the_system(auth_token=auth_token)


def get_auth_token_by_response(response):
    if 'X-Dm-Auth-Token' in response.headers:
        return response.headers['X-Dm-Auth-Token']
    else:
        raise ValueError('Токен не найден в заголовках ответа')