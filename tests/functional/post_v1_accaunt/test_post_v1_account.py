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

    account_helper.register_new_user(login=login, password=password, email=email)

    account_helper.user_login(login=login, password=password)

    # # Получение данных о пользователе
    #
    # aut_token = get_auth_token_by_login(response)
    # response = account.account_api.get_v1_account(auth_token=aut_token)
    # assert response.status_code == 200, f"Данные о пользователи не были получены {response.json()}"
    #
    # # Сброс пароля пользователя
    # json_data = {
    #     'login': login,
    #     'email': email
    # }
    # response = account.account_api.post_v1_account_password(json_data=json_data)
    # assert response.status_code == 200
    #
    # response = mail_hog.mailhog_api.get_api_v2_messages()
    # reset_token = get_reset_token_by_login(login=login, response=response)
    #
    # # Сменапароля пользователя
    # json_data = {
    #     "login": login,
    #     "token": reset_token,
    #     "oldPassword": password,
    #     "newPassword": "Qwert123"
    # }
    # response = account.account_api.put_v1_account_password(json_data=json_data)
    # assert response.status_code == 200, f"Пароль не был изменен, {response.json()}"
    #
    # # Выход
    # response = account.login_api.delete_v1_account_login(auth_token=aut_token)
    # assert response.status_code == 204, f"Выход не был выполнен, {response.json()}"


# def get_reset_token_by_login(login, response):
#     token = None
#     for item in response.json()['items']:
#         user_data = loads(item['Content']['Body'])
#         user_login = user_data['Login']
#         if user_login == login and user_data.get('ConfirmationLinkUri'):
#             token = user_data['ConfirmationLinkUri'].split('/')[-1]
#         return token
#
#
# def get_auth_token_by_login(response):
#     if 'X-Dm-Auth-Token' in response.headers:
#         return response.headers['X-Dm-Auth-Token']
#     else:
#         print('There is no token in headers')
