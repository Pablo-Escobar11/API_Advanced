import requests
import allure
from rest_client.client import RestClient


class MailhogApi(RestClient):
    @allure.step('Получить все письма')
    def get_api_v2_messages(self, limit=50):
        """
        Get users emails
        :return:
        """
        params = {
            'limit': limit,
        }
        response = self.get(path=f'/api/v2/messages', params=params, verify=False)
        return response
