import requests

from rest_client.client import RestClient


class AccountApi(RestClient):
    def __init__(self, host, headers=None):
        super().__init__(host, headers)

    def post_v1_account(self, json_data):
        """
        /v1/account
        Register new user
        :param json_data:
        :return:
        """
        response = self.post(path='/v1/account', json=json_data)
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

    def get_v1_account(self, auth_token):
        """
        GET
        /v1/account
        Get current user
        """
        headers = {
            'accept': 'text/plain',
            'X-Dm-Auth-Token': auth_token
        }
        response = self.get(path=f'/v1/account/', headers=headers)
        return response

    def post_v1_account_password(self, json_data):
        """
        POST
        /v1/account/password
        Reset registered user password
        :param json_data:
        :return:
        """

        headers = {
            'accept': 'text/plain',
        }
        response = self.post(path=f'/v1/account/password/', headers=headers, json=json_data)
        return response

    def put_v1_account_password(self, json_data):
        """
        PUT
        /v1/account/password
        Change registered user password
        :param json_data:
        :return:
        """

        headers = {
            'accept': 'text/plain',
        }
        response = self.put(path=f'/v1/account/password/', headers=headers, json=json_data)
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