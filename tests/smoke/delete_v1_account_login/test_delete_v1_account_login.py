from checkers.http_checkers import check_status_code_http
import structlog
import allure

structlog.configure(
    processors=[structlog.processors.JSONRenderer(indent=4,
                                                  ensure_ascii=True,
                                                  # sort_keys=True
                                                  )
                ]
)


@allure.suite('Тесты на проверку метода DELETE v1/account')
@allure.sub_suite('Позитивный и негативный тест')
class TestDeleteV1Account:

    @allure.title('Проверка выхода авторизованного пользователя с аккаунта')
    def test_delete_v1_account_login(self, auth_account_helper):
        response = auth_account_helper.logout_from_the_system()
        assert response.status_code == 204, f"Выход не был выполнен, {response.json()}"

    @allure.title('Проверка выхода не авторизованного пользователя с аккаунта')
    def test_delete_v1_account_login_without_auth(self, account_helper):
        with check_status_code_http(401, 'User must be authenticated'):
            account_helper.logout_from_the_system()
