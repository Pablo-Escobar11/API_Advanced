from datetime import datetime
from hamcrest import assert_that, \
    has_property, \
    starts_with, \
    all_of, \
    instance_of, \
    has_properties, \
    equal_to


class PostV1Account:
    @classmethod
    def check_response_values(cls, response, login):
        today = datetime.now().strftime('%Y-%m-%d')
        assert_that(
            response, all_of(
                has_property('resource',
                             has_properties({
                                 'login': equal_to(login),
                                 'registration': instance_of(datetime),
                                 'rating': has_properties(
                                     {

                                         "enabled": equal_to(True),
                                         "quality": equal_to(0),
                                         "quantity": equal_to(0)
                                     }
                                 )

                             }
                             )
                             )
            )
        )
        assert_that(str(response.resource.registration), starts_with(today))
