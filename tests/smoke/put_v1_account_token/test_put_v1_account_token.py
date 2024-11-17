import time
import structlog

structlog.configure(
    processors=[structlog.processors.JSONRenderer(indent=4,
                                                  ensure_ascii=True,
                                                  # sort_keys=True
                                                  )
                ]
)


def test_put_v1_account_token(account_helper, prepare_user):
    # Подготовка данных

    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    time.sleep(1)
    # Регистрация, получения письма, активация пользователя
    account_helper.register_new_user(login=login, password=password, email=email)
