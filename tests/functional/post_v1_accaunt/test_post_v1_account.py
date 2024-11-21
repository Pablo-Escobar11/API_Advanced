import structlog
from hamcrest import assert_that, \
    has_property, \
    starts_with, \
    all_of, \
    instance_of, \
    has_properties, \
    equal_to, \
    only_contains
from datetime import datetime

structlog.configure(
    processors=[structlog.processors.JSONRenderer(indent=4,
                                                  ensure_ascii=True,
                                                  # sort_keys=True
                                                  )
                ]
)


def test_post_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    # Регистрация пользователя!!!!!!!!!!!!!!!!!!!!!!!!!

    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password, validate_response=True)
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
