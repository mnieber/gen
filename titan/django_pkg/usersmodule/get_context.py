def get_context(users_module):
    _ = lambda: None
    _.django_app = users_module.django_app

    _.create_user_profile = bool(
        [x for x in _.django_app.modules if x.name == "userProfiles"]
    )

    return dict(_=_)
