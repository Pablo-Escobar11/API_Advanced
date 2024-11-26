from datetime import datetime

from hamcrest import assert_that, \
    has_property, \
    starts_with, \
    all_of, \
    instance_of, \
    has_properties, \
    only_contains, \
    greater_than_or_equal_to
from dm_api_account.models.user_envelope import UserRole


class GetV1Account:
    @classmethod
    def check_response_value(cls, response):
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
