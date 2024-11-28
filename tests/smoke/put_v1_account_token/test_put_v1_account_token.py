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


@allure.suite('Тесты на проверку метода PUT v1/account/token')
@allure.sub_suite('Позитивный тест')
class TestPutV1AccountToken:

    @allure.title('Проверка активатиции пользователя')
    def test_put_v1_account_token(self, account_helper, prepare_user):
        # Подготовка данных

        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        # Регистрация, получения письма, активация пользователя
        account_helper.register_new_user(login=login, password=password, email=email)
