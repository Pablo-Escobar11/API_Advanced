import time
from collections import namedtuple
from datetime import datetime

import pytest
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


@pytest.fixture(scope="session")
def mailhog_api():
    mail_configuration = MailHogConfiguration(host='http://5.63.153.31:5025')
    mail_hog_client = MailHogapi(configuration=mail_configuration)
    return mail_hog_client


@pytest.fixture(scope="session")
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture(scope="session")
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mail_hog=mailhog_api)
    return account_helper


@pytest.fixture(scope="module")
def auth_account_helper(mailhog_api):
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    auth_account_helper = AccountHelper(dm_account_api=account, mail_hog=mailhog_api)
    auth_account_helper.auth_client(login="pasha_test", password="Xdvgy4321")
    return auth_account_helper


@pytest.fixture()
def prepare_user():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%m_%d_%H_%M_%S")
    login = f'pasha_{formatted_time}'
    email = f'{login}@mail.ru'
    password = 'Qwerty123'
    new_password = 'Qwert4321'
    new_email = f'new{email}'
    User = namedtuple("User", ["login", "password", "email", "new_password", "new_email"])
    user = User(login=login, password=password, new_password=new_password, email=email, new_email=new_email)
    return user
