import time
import structlog

structlog.configure(
    processors=[structlog.processors.JSONRenderer(indent=4,
                                                  ensure_ascii=True,
                                                  # sort_keys=True
                                                  )
                ]
)


def test_post_v1_account_login(account_helper, prepare_user):
    # Подготовка данных

    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    time.sleep(1)

    # Регистрация пользователя и вход в аккаунт
    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 200, f'Пользователь не авторизован {response.json()}'
