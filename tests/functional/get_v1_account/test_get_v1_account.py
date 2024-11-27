from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http
import allure


@allure.suite('Тесты на проверку метода GET v1/account')
@allure.sub_suite('Позитивный и негативный тест на получение данных о пользователя')
class TestGetV1Account:
    @allure.title('Получение данных об авторизованном пользователе')
    def test_get_v1_account_auth(self, auth_account_helper):
        response = auth_account_helper.get_user_info(validate_response=True)
        GetV1Account.check_response_value(response)

    @allure.title('Попытка получения данных о не авторизованном пользователе')
    def test_get_v1_account_no_auth(self, account_helper):
        with check_status_code_http(401, 'User must be authenticated'):
            account_helper.get_user_info()
