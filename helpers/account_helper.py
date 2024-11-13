import time
from json import loads

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogapi


class AccountHelper:
    def __init__(self, dm_account_api: DMApiAccount, mail_hog: MailHogapi):
        self.dm_account_api = dm_account_api
        self.mail_hog = mail_hog

    def register_new_user(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        time.sleep(1)
        # Регистрация пользователя!!!!!!!!!!!!!!!!!!!!!!!!!
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"Пользователь не был создан, {response.json()}"

        # Получить токен !!!!!!!!!!!
        activate_token = self.get_activation_token_by_login(login=login)
        assert activate_token is not None, f"Токен для пользователя {login} не был получен"

        # Активация пользователя
        response = self.dm_account_api.account_api.put_v1_account_token(token=activate_token)
        assert response.status_code == 200, f'Пользователь не активен {response.json()}'
        return response

    def user_login(self, login: str, password: str, remember_me: bool = True):
        # Авторизация !!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }

        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, f'Пользователь не авторизован {response.json()}'
        return response

    def get_user_info(self, login: str, password: str):
        auth_token = self.get_auth_token_by_login(self.user_login(login=login, password=password))
        response = self.dm_account_api.account_api.get_v1_account(auth_token=auth_token)
        assert response.status_code == 200, f"Данные о пользователи не были получены {response.json()}"
        return response

    def reset_and_change_password(self, login: str, email: str, old_password: str, new_password):
        # Сброс пароля пользователя
        json_data = {
            'login': login,
            'email': email
        }
        response = self.dm_account_api.account_api.post_v1_account_password(json_data=json_data)
        assert response.status_code == 200

        # Получение токена
        response = self.mail_hog.mailhog_api.get_api_v2_messages()
        reset_token = self.get_reset_password_token_by_login(response=response, login=login)

        # Смена пароля пользователя

        json_data = {
            "login": login,
            "token": reset_token,
            "oldPassword": old_password,
            "newPassword": new_password
        }
        self.dm_account_api.account_api.put_v1_account_password(json_data=json_data)
        assert response.status_code == 200, f"Пароль не был изменен, {response.json()}"
        return response

    # Смена почты
    def change_register_user_email(self, login, password, new_email):
        json_data = {
            "login": login,
            "password": password,
            "email": new_email
        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, f'Запрос на сброс почты не отправлен, {response.json()}'
        return response

    def login_user_to_the_system_without_confirm_email(self, login, password, remember_me=True):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }

        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 403, f'Пользователь не авторизован {response.json()}'
        return response

    def get_messages_and_confirm_new_email(self, login, new_email):
        # Получение письма
        response = self.mail_hog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, f"Письма не были получены, {response.json()}"

        # Получение токена для почты
        token = self.get_reset_token_for_email(login=login, response=response, email=new_email)

        # Подтверждение новой почты
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f"Почта не иизменена, {response.json()}"
        return response

    def logaut_from_the_system(self, password, login):
        response = self.user_login(password=password, login=login)
        auth_token = self.get_auth_token_by_login(response=response)

        response = self.dm_account_api.login_api.delete_v1_account_login(auth_token=auth_token)
        assert response.status_code == 204, f"Выход не был выполнен, {response.json()}"
        return response

    def get_activation_token_by_login(self, login):
        response = self.mail_hog.mailhog_api.get_api_v2_messages()
        token = None
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            return token

    @staticmethod
    def get_auth_token_by_login(response):
        if 'X-Dm-Auth-Token' in response.headers:
            return response.headers['X-Dm-Auth-Token']
        else:
            print('There is no token in headers')

    @staticmethod
    def get_reset_password_token_by_login(login, response):
        token = None
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login and user_data.get('ConfirmationLinkUri'):
                token = user_data['ConfirmationLinkUri'].split('/')[-1]
            return token

    @staticmethod
    def get_reset_token_for_email(login, response, email):
        token = None
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login and email == item['Content']['Headers']['To'][0]:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            return token
