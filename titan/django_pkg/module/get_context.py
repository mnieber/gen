import ramda as R
from moonleap.utils.case import sn
from titan.django_pkg.graphene_django.utils import find_module_that_provides_item_list


def get_context(module):
    _ = lambda: None
    _.django_app = module.django_app

    def comp(lhs_model, rhs_model):
        for fk_field in lhs_model.fk_fields:
            if fk_field.target == rhs_model.name:
                return +1
        for fk_field in rhs_model.fk_fields:
            if fk_field.target == lhs_model.name:
                return -1
        return 0

    _.django_models = R.sort(comp, module.django_models)

    class Sections:
        def model_imports(self, django_model):
            result = []
            targets = []
            for fk_field in django_model.fk_fields:
                targets.append(fk_field.target)

            for many_to_many_field in django_model.many_to_many_fields:
                targets.append(many_to_many_field.target)

            for target in targets:
                provider_module = find_module_that_provides_item_list(
                    _.django_app, target
                )
                if provider_module and provider_module is not module:
                    result.append(
                        f"from {sn(provider_module.name)}.models import {target}"
                    )
            return "\n".join(result)

    return dict(sections=Sections(), _=_)
