import time
from json import loads
from datetime import datetime

from dm_api_account.apis.account_api import AccountApi
from api_mailhog.apis.mail_hog_api import MailhogApi
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


def test_put_v1_account_token():
    mail_configuration = MailHogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    # Подготовка данных
    account = DMApiAccount(configuration=dm_api_configuration)
    mail_hog = MailHogapi(configuration=mail_configuration)

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
    # Регистрация, получения письма, активация пользователя

    account_helper = AccountHelper(mail_hog=mail_hog, dm_account_api=account)
    account_helper.register_new_user(login=login, password=password, email=email)
