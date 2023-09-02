from titan.api_pkg.apiregistry.get_form_type_specs import get_form_type_specs
from titan.api_pkg.apiregistry.get_public_type_specs import get_public_type_specs


def get_helpers(_):
    class Helpers:
        public_type_specs = get_public_type_specs(
            _.api_reg,
            include_stubs=False,
            predicate=lambda type_spec: not type_spec.no_api,
        )
        form_type_specs = get_form_type_specs(_.api_reg)

    return Helpers()
