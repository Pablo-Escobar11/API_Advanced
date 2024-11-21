import requests

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.user_envelope import UserEnvelope
from rest_client.client import RestClient


class LoginApi(RestClient):

    def post_v1_account_login(self, login_credentials: LoginCredentials, validate_response=True):
        """
        POST
        /v1/account/login
        Authenticate via credentials
        :param validate_response:
        :param login_credentials:
        :param json_data:
        :return:
        """
        response = self.post(path=f'/v1/account/login', json=login_credentials.model_dump(exclude_none=True, by_alias=True))
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def delete_v1_account_login(self, **kwargs):
        """
        DELETE
        /v1/account/login
        Logout as current user
        :param auth_token:
        :return:
        """

        response = self.delete(path=f'/v1/account/login', **kwargs)
        return response

    def delete_v1_account_login_all(self, **kwargs):
        """
        DELETE
        /v1/account/login/all
        Logout from every device
        :param auth_token:
        :return:
        """

        response = self.delete(path=f'/v1/account/login/all', **kwargs)
        return response
