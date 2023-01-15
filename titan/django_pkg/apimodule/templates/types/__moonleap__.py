from titan.api_pkg.apiregistry.get_form_type_specs import get_form_type_specs
from titan.api_pkg.apiregistry.get_public_type_specs import get_public_type_specs


def get_helpers(_):
    class Helpers:
        public_type_specs = get_public_type_specs(
            _.api_reg,
            include_stubs=False,
            predicate=lambda field_spec: "server" in field_spec.has_api,
        )
        public_type_specs_provided_by_django = [
            x for x in public_type_specs if x.django_module
        ]
        form_type_specs = get_form_type_specs(_.api_reg)

    return Helpers()
