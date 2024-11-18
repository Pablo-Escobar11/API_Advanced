import structlog

structlog.configure(
    processors=[structlog.processors.JSONRenderer(indent=4,
                                                  ensure_ascii=True,
                                                  # sort_keys=True
                                                  )
                ]
)


def test_get_v1_account_auth(auth_account_helper):
    response = auth_account_helper.get_user_info()
    assert response.status_code == 200, f"Данные о пользователи не получены, {response.json()}"


def test_get_v1_account_no_auth(account_helper):
    response = account_helper.get_user_info()
    assert response.status_code == 401, (f"Данные о пользователи получены, однако пользователь не авторизован,"
                                         f" {response.json()}")
