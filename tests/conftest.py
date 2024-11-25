import time
from collections import namedtuple
from datetime import datetime
from pathlib import Path
import pytest
import structlog
from vyper import v
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


@pytest.fixture(scope='session', autouse=True)
def set_config(request):
    config = Path(__file__).joinpath("../../").joinpath("config")
    config_name = request.config.getoption("--env")
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f"{option}", request.config.getoption(f"--{option}"))


options = (
    'service.dm_api_account',
    'service.mailhog',
    'user.login',
    'user.password'
)


def pytest_addoption(parser):
    parser.addoption('--env', action='store', default='stg', help='run stg')
    for option in options:
        parser.addoption(f"--{option}", action="store", default=None)


@pytest.fixture(scope="session")
def mailhog_api():
    mail_configuration = MailHogConfiguration(host=v.get("service.mailhog"))
    mail_hog_client = MailHogapi(configuration=mail_configuration)
    return mail_hog_client


@pytest.fixture(scope="session")
def account_api():
    dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"), disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture(scope="session")
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mail_hog=mailhog_api)
    return account_helper


@pytest.fixture(scope="module")
def auth_account_helper(mailhog_api):
    dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"), disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    auth_account_helper = AccountHelper(dm_account_api=account, mail_hog=mailhog_api)
    auth_account_helper.auth_client(login=v.get("user.login"), password=v.get("user.password"))
    return auth_account_helper


@pytest.fixture()
def prepare_user():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%m_%d_%H_%M_%S")
    login = f'pasha_{formatted_time}'
    email = f'{login}@mail.ru'
    password = v.get("user.password")
    new_password = 'Qwert4321'
    new_email = f'new{email}'
    User = namedtuple("User", ["login", "password", "email", "new_password", "new_email"])
    user = User(login=login, password=password, new_password=new_password, email=email, new_email=new_email)
    return user
