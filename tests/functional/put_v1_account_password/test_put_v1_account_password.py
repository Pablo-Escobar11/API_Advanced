import structlog
import allure

structlog.configure(
    processors=[structlog.processors.JSONRenderer(indent=4,
                                                  ensure_ascii=True,
                                                  # sort_keys=True
                                                  )
                ]
)


@allure.suite('Тесты на проверку метода PUT v1/account')
@allure.sub_suite('Позитивный тест')
class TestPutV1Account:
    @allure.title('Проверка смены пароля и вход пользователя в аккаунт')
    def test_put_v1_account_password(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        new_password = prepare_user.new_password
        email = prepare_user.email

        # Реистрация и вход пользователя в аккаунт
        account_helper.register_new_user(login=login, password=password, email=email)
        account_helper.user_login(login=login, password=password)

        account_helper.reset_and_change_password(new_password=new_password, old_password=password, email=email,
                                                 login=login)
