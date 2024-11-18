import structlog

structlog.configure(
    processors=[structlog.processors.JSONRenderer(indent=4,
                                                  ensure_ascii=True,
                                                  # sort_keys=True
                                                  )
                ]
)


def test_put_v1_account_password(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    new_password = prepare_user.new_password
    email = prepare_user.email

    # Реистрация и вход пользователя в аккаунт
    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.auth_client(login=login, password=password)

    response = account_helper.reset_and_change_password(new_password=new_password, old_password=password, email=email,
                                                        login=login)
    assert response.status_code == 200, f"Пароль не был изменен, {response.json()}"
