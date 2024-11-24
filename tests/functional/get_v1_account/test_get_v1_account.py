import structlog
from datetime import datetime
from dm_api_account.models.user_envelope import UserRole
from hamcrest import assert_that, \
    has_property, \
    starts_with, \
    all_of, \
    instance_of, \
    has_properties, \
    equal_to, \
    only_contains, \
    greater_than_or_equal_to, \
    has_value

structlog.configure(
    processors=[structlog.processors.JSONRenderer(indent=4,
                                                  ensure_ascii=True,
                                                  # sort_keys=True
                                                  )
                ]
)


def test_get_v1_account_auth(auth_account_helper):
    response = auth_account_helper.get_user_info(validate_response=True)
    print(response)
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
    response = account_helper.get_user_info()
    assert response.status_code == 401, (f"Данные о пользователи получены, однако пользователь не авторизован,"
                                         f" {response.json()}")
