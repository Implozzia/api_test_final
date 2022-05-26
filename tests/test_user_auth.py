import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

LOGIN_LINK = 'https://playground.learnqa.ru/api/user/login'
AUTH_LINK = 'https://playground.learnqa.ru/api/user/auth'


class TestUserAuth(BaseCase):
    exclude_params = [
        ('no_cookie'),
        ('no_token')
    ]

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_login = requests.post(LOGIN_LINK, data=data)

        self.auth_sid = self.get_cookie(response_login, 'auth_sid')
        self.token = self.get_header(response_login, 'x-csrf-token')
        self.user_id_from_response_method = self.get_json_value(response_login, 'user_id')

    def test_auth_user(self):
        response_check = requests.get(
            AUTH_LINK,
            cookies={'auth_sid': self.auth_sid},
            headers={'x-csrf-token': self.token})

        Assertions.assert_json_value_by_name(
            response_check,
            'user_id',
            self.user_id_from_response_method,
            'User id from auth method is not equal to iser id from check method')

    @pytest.mark.parametrize('conditions', exclude_params)
    def test_negative_auth_check(self, conditions):
        if conditions == 'no_cookie':
            response_check = requests.get(AUTH_LINK, headers={'x-csrf-token': self.token})
        else:
            response_check = requests.get(AUTH_LINK, cookies={'auth_sid': self.auth_sid})

        Assertions.assert_json_value_by_name(
            response_check,
            'user_id',
            0,
            f'User is authorised with condition {conditions}'
        )