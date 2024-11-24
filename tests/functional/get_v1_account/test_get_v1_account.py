from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http


def test_get_v1_account_auth(auth_account_helper):
    response = auth_account_helper.get_user_info(validate_response=True)
    GetV1Account.check_response_value_get_v1_account(response)


def test_get_v1_account_no_auth(account_helper):
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.get_user_info()
