def test_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    new_password = prepare_user.new_password
    email = prepare_user.email
    # Регистрация пользователя!!!!!!!!!!!!!!!!!!!!!!!!!

    account_helper.register_new_user(login=login, password=password, email=email)

    response = account_helper.user_login(login=login, password=password)
    auth_token = get_auth_token_by_response(response=response)

    # Сброс и смена пароля пользователя
    account_helper.reset_and_change_password(email=email, new_password=new_password, old_password=password, login=login)

    # Вход с новым паролем

    response = account_helper.user_login(login=login, password=new_password)
    assert response.status_code == 200, f'Пользователь не авторизован {response.json()}'

    # Выход
    account_helper.logout_from_the_system(auth_token=auth_token)


def get_auth_token_by_response(response):
    return response.headers.get('X-Dm-Auth-Token') or ValueError('Токен не найден в заголовках ответа')
