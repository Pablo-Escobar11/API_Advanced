import allure
import requests

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.new_password_credentials import NewPasswordCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_credentials import ResetCredentials
from dm_api_account.models.reset_email import ResetEmail
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from rest_client.client import RestClient


class AccountApi(RestClient):
    @allure.step('Зарегистрировать нового пользователя')
    def post_v1_account(self, registration: Registration):
        """
        /v1/account
        Register new user
        :param registration:
        :return:
        """
        response = self.post(path='/v1/account', json=registration.model_dump(exclude_none=True, by_alias=True))
        return response

    @allure.step('Активировать нового пользователя')
    def put_v1_account_token(self, token, validate_response=True):
        """
        PUT
        /v1/account/{token}
        Activate registered user
        :param token:
        :return:
        """
        headers = {
            'accept': 'text/plain',
        }
        response = self.put(path=f'/v1/account/{token}', headers=headers)
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step('Получение информации о пользователи')
    def get_v1_account(self, validate_response=True, **kwargs):
        """
        GET
        /v1/account
        Get current user
        """
        response = self.get(path=f'/v1/account/', **kwargs)
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response

    @allure.step('Сброс пароля')
    def post_v1_account_password(self, reset_credentials: ResetCredentials, validate_response=True):
        """
        POST
        /v1/account/password
        Reset registered user password
        :param validate_response:
        :param reset_credentials:
        :param json_data:
        :return:
        """

        headers = {
            'accept': 'text/plain',
        }
        response = self.post(path=f'/v1/account/password/', headers=headers,
                             json=reset_credentials.model_dump(exclude_none=True, by_alias=True))
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response

    @allure.step("Смена пароля")
    def put_v1_account_password(self, new_password_credentials: NewPasswordCredentials, auth_token=None,
                                validate_response=True):
        """
        PUT
        /v1/account/password
        Change registered user password
        :param validate_response:
        :param new_password_credentials:
        :param auth_token:
        :param json_data:
        :return:
        """

        headers = {
            'accept': 'text/plain',
            'X-Dm-Auth-Token': auth_token

        }
        response = self.put(path=f'/v1/account/password/', json=new_password_credentials.model_dump(exclude_none=True,
                                                                                                    by_alias=True), headers=headers)
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response

    @allure.step('Смена почты')
    def put_v1_account_email(self, reset_email: ResetEmail, validate_response=True):
        """
        PUT
        /v1/account/email
        Change registered user email
        :param reset_email:
        :param json_data:
        :return:
        """
        headers = {
            'accept': 'text/plain',
        }

        response = self.put(path=f'/v1/account/email/', headers=headers, json=reset_email.model_dump(exclude_none=True,
                                                                                                     by_alias=True))
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response
