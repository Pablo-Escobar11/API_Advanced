from time import sleep

import structlog

structlog.configure(
    processors=[structlog.processors.JSONRenderer(indent=4,
                                                  ensure_ascii=True,
                                                  # sort_keys=True
                                                  )
                ]
)
sleep(3)


def test_delete_v1_account_login_all(auth_account_helper):
    response = auth_account_helper.logout_from_the_system_all()
    assert response.status_code == 204, f"Выход не был выполнен, {response.json()}"


def test_delete_v1_account_login_all_without_auth(account_helper):
    response = account_helper.logout_from_the_system_all()
    assert response.status_code == 401, "Выход выполнен для не авторизованного пользователя"
