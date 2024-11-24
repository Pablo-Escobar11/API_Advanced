from contextlib import contextmanager
import requests
from requests.exceptions import HTTPError


@contextmanager
def check_status_code_http(expected_status_code: requests.codes = requests.codes.OK, expected_message: str = ''):
    try:
        yield
        if expected_status_code != requests.codes.OK:
            raise AssertionError(f"Ожидыемый статус код должен быть равен {expected_status_code}")
        if expected_message:
            raise AssertionError(f"Должно быть получено сообщение {expected_message}, но запрос прошел умпешно")
    except HTTPError as err:
        assert err.response.status_code == expected_status_code
        assert err.response.json()['title'] == expected_message


@contextmanager
def check_status_code_http_and_error(
        expected_status_code, expected_message, field
        ):
    try:
        yield
    except HTTPError as err:
        assert err.response.status_code == expected_status_code
        assert err.response.json()['errors'][field][0] == expected_message
