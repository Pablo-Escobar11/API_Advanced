import requests

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_credentials import ResetCredentials
from rest_client.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(self, registration: Registration):
        """
        /v1/account
        Register new user
        :param registration:
        :return:
        """
        response = self.post(path='/v1/account', json=registration.model_dump(exclude_none=True, by_alias=True))
        return response

    def put_v1_account_token(self, token):
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
        return response

    def get_v1_account(self, **kwargs):
        """
        GET
        /v1/account
        Get current user
        """
        response = self.get(path=f'/v1/account/', **kwargs)
        return response

    def post_v1_account_password(self, reset_credentials: ResetCredentials):
        """
        POST
        /v1/account/password
        Reset registered user password
        :param reset_credentials:
        :param json_data:
        :return:
        """

        headers = {
            'accept': 'text/plain',
        }
        response = self.post(path=f'/v1/account/password/', headers=headers,
                             json=reset_credentials.model_dump(exclude_none=True, by_alias=True))
        return response

    def put_v1_account_password(self, json_data, auth_token=None):
        """
        PUT
        /v1/account/password
        Change registered user password
        :param auth_token:
        :param json_data:
        :return:
        """

        headers = {
            'accept': 'text/plain',
            'X-Dm-Auth-Token': auth_token

        }
        response = self.put(path=f'/v1/account/password/', json=json_data, headers=headers)
        return response

    def put_v1_account_email(self, json_data):
        """
        PUT
        /v1/account/email
        Change registered user email
        :param json_data:
        :return:
        """
        headers = {
            'accept': 'text/plain',
        }

        response = self.put(path=f'/v1/account/email/', headers=headers, json=json_data)
        return response
