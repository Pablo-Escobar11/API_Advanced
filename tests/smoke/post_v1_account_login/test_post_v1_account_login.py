import time
import structlog
import allure

structlog.configure(
    processors=[structlog.processors.JSONRenderer(indent=4,
                                                  ensure_ascii=True,
                                                  # sort_keys=True
                                                  )
                ]
)


@allure.suite('Тесты на проверку метода POST v1/login')
@allure.sub_suite('Позитивный тест')
class TestPostV1AccountLogin:
    @allure.title('Проверка входа в аккаунт авторизованного пользователя')
    def test_post_v1_account_login(self, account_helper, prepare_user):
        # Подготовка данных

        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password
        time.sleep(1)

        # Регистрация пользователя и вход в аккаунт
        account_helper.register_new_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password)
        assert response.status_code == 200, f'Пользователь не авторизован {response.json()}'
