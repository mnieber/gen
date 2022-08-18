import ramda as R
from moonleap.utils.fp import add_to_list_as_set


def comp(lhs_model, rhs_model):
    for field_spec in lhs_model.type_spec.get_field_specs(["fk", "relatedSet"]):
        if field_spec.target == rhs_model.name:
            return +1
    for field_spec in rhs_model.type_spec.get_field_specs(["fk", "relatedSet"]):
        if field_spec.target == lhs_model.name:
            return -1
    return 0


def get_helpers(_):
    class Helpers:
        django_app = _.module.django_app
        django_models = R.sort(comp, _.module.django_models)

        @property
        def items_to_import(self):
            result = []
            for django_model in self.django_models:
                for field_spec in django_model.type_spec.get_field_specs(
                    ["fk", "relatedSet"]
                ):
                    item = field_spec.target_item
                    if item.django_module is not _.module:
                        add_to_list_as_set(result, item)
            return result

    return Helpers()
