def get_context(users_module):
    _ = lambda: None
    _.django_app = users_module.django_app

    return dict(_=_, django_app=users_module.django_app, module=users_module)
