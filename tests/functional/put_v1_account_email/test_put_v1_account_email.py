import time
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
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 403, f'Пользователь авторизован {response.json()}'

    # Получение письма и подтверждение новой почты
    account_helper.get_messages_and_confirm_new_email(login=login, new_email=new_email)

    # Логин пользвателя в систему
    response = account_helper.user_login(login=login, password=password)

    assert response.status_code == 200, f'Пользователь не авторизован {response.json()}'


def get_auth_token_by_response(response):
    return response.headers.get('X-Dm-Auth-Token') or ValueError('Токен не найден в заголовках ответа')
