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
