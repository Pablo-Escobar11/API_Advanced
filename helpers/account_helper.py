import time
from json import loads

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.new_password_credentials import NewPasswordCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_credentials import ResetCredentials
from dm_api_account.models.reset_email import ResetEmail
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogapi


# from retrying import retry
#
#
# def retry_if_result_none(result):
#     return result is None


def retrier(func):
    def wrapper(*args, **kwargs):
        token = None
        count = 0
        while token is None:
            token = func(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError("Превышено количество попыток получения токена")
            if token:
                return token
            time.sleep(1)

    return wrapper


class AccountHelper:
    def __init__(self, dm_account_api: DMApiAccount, mail_hog: MailHogapi):
        self.dm_account_api = dm_account_api
        self.mail_hog = mail_hog

    def register_new_user(self, login: str, password: str, email: str, activated: bool = True, validate_response=False):
        registration = Registration(
            login=login,
            email=email,
            password=password,
        )
        time.sleep(1)
        # Регистрация пользователя!!!!!!!!!!!!!!!!!!!!!!!!!
        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f"Пользователь не был создан, {response.json()}"

        # Активация пользователя
        if activated:
            # Получить токен !!!!!!!!!!!
            activate_token = self.get_activation_token_by_login(login=login)
            assert activate_token is not None, f"Токен для пользователя {login} не был получен"
            response = self.dm_account_api.account_api.put_v1_account_token(token=activate_token)
        return response

    def user_login(self, login: str, password: str, remember_me: bool = True, validate_response=False):
        # Авторизация !!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        login_credentials = LoginCredentials(
            login=login,
            password=password,
            rememberMe=remember_me,
        )

        response = self.dm_account_api.login_api.post_v1_account_login(login_credentials=login_credentials,
                                                                       validate_response=validate_response)
        return response

    def auth_client(self, login: str, password: str):
        response = self.user_login(login=login, password=password)
        auth_token = {
            'X-Dm-Auth-Token': response.headers['X-Dm-Auth-Token']}
        self.dm_account_api.login_api.set_headers(auth_token)
        self.dm_account_api.account_api.set_headers(auth_token)

    def get_user_info(self, validate_response=False, **kwargs):
        response = self.dm_account_api.account_api.get_v1_account(validate_response=validate_response, **kwargs)
        return response

    def reset_and_change_password(self, login: str, email: str, old_password: str, new_password, validate_response=False):
        response = self.user_login(login=login, password=old_password)
        auth_token = response.headers.get('X-Dm-Auth-Token')
        assert auth_token, 'Токен не найден в заголовках ответа'
        # Сброс пароля пользователя
        reset_credentials = ResetCredentials(
            login=login,
            email=email
        )
        self.dm_account_api.account_api.post_v1_account_password(reset_credentials=reset_credentials)

        # Получение токена
        response = self.mail_hog.mailhog_api.get_api_v2_messages()
        reset_token = self.get_reset_update_token_for_password_or_login(response=response, login=login)

        # Смена пароля пользователя

        new_password_credentials = NewPasswordCredentials(
            login=login,
            token=reset_token,
            oldPassword=old_password,
            newPassword=new_password
        )
        response = self.dm_account_api.account_api.put_v1_account_password(new_password_credentials=new_password_credentials,
                                                                           auth_token=auth_token)
        return response

    # Смена почты
    def change_register_user_email(self, login, password, new_email):
        reset_email = ResetEmail(
            login=login,
            password=password,
            email=new_email
        )
        response = self.dm_account_api.account_api.put_v1_account_email(reset_email=reset_email)
        return response

    #Метод для получения письма затем получения токена для активации смены почты и подтверждение новой почты
    def get_messages_and_confirm_new_email(self, login, new_email):
        # Получение письма
        response = self.mail_hog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, f"Письма не были получены, {response.json()}"

        # Получение токена для почты
        token = self.get_reset_update_token_for_password_or_login(login=login, response=response, email=new_email)

        # Подтверждение новой почты
        response_activated_account = self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response_activated_account

    #Выход из аккаунта
    def logout_from_the_system(self, **kwargs):
        response = self.dm_account_api.login_api.delete_v1_account_login(**kwargs)
        return response

    #Выход из аккаунта со всех устройств
    # def logout_from_the_system_all(self):
    #     response = self.dm_account_api.login_api.delete_v1_account_login_all()
    #     return response
    def logout_from_the_system_all(self, token=None):
        if token:
            headers = {'token': token}
            response = self.dm_account_api.login_api.delete_v1_account_login_all(headers)
            return response
        response = self.dm_account_api.login_api.delete_v1_account_login_all()
        return response

    @retrier
    # @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
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
    def get_reset_update_token_for_password_or_login(login, response, email=None):
        token = None
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']

            if email:
                # Логика для проверки email, для подтверждения смены почты
                if user_login == login and email == item['Content']['Headers']['To'][0]:
                    token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            else:
                # Логика для проверки логина, для смены пароля
                if user_login == login and user_data.get('ConfirmationLinkUri'):
                    token = user_data['ConfirmationLinkUri'].split('/')[-1]

            if token:
                break

        return token
