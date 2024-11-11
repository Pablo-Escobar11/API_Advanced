import requests

from rest_client.client import RestClient


class LoginApi(RestClient):

    def post_v1_account_login(self, json_data):
        """
        POST
        /v1/account/login
        Authenticate via credentials
        :param json_data:
        :return:
        """
        response = self.post(path=f'/v1/account/login', json=json_data)
        return response

    def delete_v1_account_login(self, auth_token):
        """
        DELETE
        /v1/account/login
        Logout as current user
        :param auth_token:
        :return:
        """
        headers = {
            'X-Dm-Auth-Token': auth_token
        }

        response = self.delete(path=f'/v1/account/login', headers=headers)
        return response

    def delete_v1_account_login_all(self, auth_token):
        """
        DELETE
        /v1/account/login/all
        Logout from every device
        :param auth_token:
        :return:
        """
        headers = {
            'X-Dm-Auth-Token': auth_token
        }

        response = self.delete(path=f'/v1/account/login/all', headers=headers)
        return response
