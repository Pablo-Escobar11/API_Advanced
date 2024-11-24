from datetime import datetime

from checkers.http_checkers import check_status_code_http
from dm_api_account.models.user_envelope import UserRole
from hamcrest import assert_that, \
    has_property, \
    starts_with, \
    all_of, \
    instance_of, \
    has_properties, \
    equal_to, \
    only_contains, \
    greater_than_or_equal_to


def test_get_v1_account_auth(auth_account_helper):
    response = auth_account_helper.get_user_info(validate_response=True)
    assert_that(
        response, all_of(
            has_property('resource',
                         has_properties({
                             'login': starts_with('pasha_test'),
                             'registration': instance_of(datetime),
                             'roles': all_of(
                                 only_contains(
                                     UserRole.GUEST,
                                     UserRole.PLAYER,
                                     UserRole.ADMINISTRATOR,
                                     UserRole.NANNY_MODERATOR,
                                     UserRole.SENIOR_MODERATOR
                                 )
                             ),
                             'rating': has_properties(
                                 enabled=True,
                                 quality=greater_than_or_equal_to(0),
                                 quantity=greater_than_or_equal_to(0)

                             )
                         }
                         )
                         )
        )
    )


def test_get_v1_account_no_auth(account_helper):
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.get_user_info()

