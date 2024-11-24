import time

import structlog
from checkers.http_checkers import check_status_code_http

structlog.configure(
    processors=[structlog.processors.JSONRenderer(indent=4,
                                                  ensure_ascii=True,
                                                  # sort_keys=True
                                                  )
                ]
)


def test_put_v1_account_email(account_helper, prepare_user):
    # Подготовка данных
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    new_email = prepare_user.new_email

    time.sleep(1)
    # Регистрация пользвателя
    account_helper.register_new_user(login=login, password=password, email=email, activated=False)

    # Смена почты
    account_helper.change_register_user_email(new_email=new_email, password=password, login=login)

    # Логин пользвателя в систему после смены почты
    with check_status_code_http(403, 'User is inactive. Address the technical support for more details'):
        account_helper.user_login(login=login, password=password)

    # Получение письма и подтверждение новой почты
    account_helper.get_messages_and_confirm_new_email(login=login, new_email=new_email)

    # Логин пользвателя в систему
    response = account_helper.user_login(login=login, password=password)

    assert response.status_code == 200, f'Пользователь не авторизован {response.json()}'
