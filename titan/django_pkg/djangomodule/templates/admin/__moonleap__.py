def get_helpers(_):
    class Helpers:
        data = []

        def __init__(self):
            self.data = self.get_data()

        def get_data(self):
            result = []
            for django_model in _.module.django_models:
                item_list = django_model.item_list
                type_spec = django_model.type_spec
                data = dict(
                    type_spec=type_spec,
                    create_inline_model=self.get_create_inline_model(type_spec),
                )
                result.append((item_list, data))
            return result

        def get_create_inline_model(self, type_spec):
            return False

    return Helpers()
