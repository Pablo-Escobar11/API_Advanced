from time import sleep

import structlog

structlog.configure(
    processors=[structlog.processors.JSONRenderer(indent=4,
                                                  ensure_ascii=True,
                                                  # sort_keys=True
                                                  )
                ]
)


def test_delete_v1_account_login(auth_account_helper):
    response = auth_account_helper.logout_from_the_system()
    assert response.status_code == 204, f"Выход не был выполнен, {response.json()}"


def test_delete_v1_account_login_without_auth(account_helper):
    response = account_helper.logout_from_the_system()
    assert response.status_code == 401, "Выход выполнен для не авторизованного пользователя"
