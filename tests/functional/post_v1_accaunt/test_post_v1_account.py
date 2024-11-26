import pytest
import structlog
from checkers.http_checkers import check_status_code_http_and_error
from checkers.post_v1_account import PostV1Account

structlog.configure(
    processors=[structlog.processors.JSONRenderer(indent=4,
                                                  ensure_ascii=True,
                                                  # sort_keys=True
                                                  )
                ]
)


def test_post_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    # Регистрация пользователя!!!!!!!!!!!!!!!!!!!!!!!!!

    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password, validate_response=True)
    PostV1Account.check_response_values(response, login)


@pytest.mark.parametrize('login, email, password, error_message, incorrect_field', [
    ('pasha_test3345', 'test@mail.com', 'Qwert', 'Short', 'Password'),
    ('pasha_test3345', 'testmail.com', 'Qwert123', 'Invalid', 'Email'),
    ('p', 'test@mail.com', 'Qwert123', 'Short', 'Login')

])
def test_post_v1_account_with_incorrect_data(account_helper, login, email, password, error_message, incorrect_field):
    with check_status_code_http_and_error(400, error_message, incorrect_field):
        account_helper.register_new_user(login=login, password=password, email=email, activated=False)
