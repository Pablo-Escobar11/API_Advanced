from rest_client.configuration import Configuration
from api_mailhog.apis.mail_hog_api import MailhogApi


class MailHogapi:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.mailhog_api = MailhogApi(configuration=self.configuration)
