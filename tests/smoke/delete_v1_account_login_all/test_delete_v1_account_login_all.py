import structlog
import allure
from checkers.http_checkers import check_status_code_http

structlog.configure(
    processors=[structlog.processors.JSONRenderer(indent=4,
                                                  ensure_ascii=True,
                                                  # sort_keys=True
                                                  )
                ]
)


@allure.suite('Тесты на проверку метода DELETE v1/account/all')
@allure.sub_suite('Позитивный и негативный тест')
class TestDeleteV1AccountLoginAll:
    @allure.title('Проверка выхода авторизованного пользователя с аккаунта со всех устройств')
    def test_delete_v1_account_login_all(self, auth_account_helper):
        response = auth_account_helper.logout_from_the_system_all()
        assert response.status_code == 204, f"Выход не был выполнен, {response.json()}"

    @allure.title('Проверка выхода не авторизованного пользователя с аккаунта со всех устройств')
    def test_delete_v1_account_login_all_without_auth(self, account_helper):
        with check_status_code_http(401, 'User must be authenticated'):
            account_helper.logout_from_the_system_all()
