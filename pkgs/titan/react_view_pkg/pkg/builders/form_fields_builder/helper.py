import ramda as R
from titan.react_view_pkg.pkg.builders.form_state_provider_builder.get_fields import (
    get_fields,
)
from titan.types_pkg.typeregistry import get_type_reg

from moonleap import u0


class Helper:
    def __init__(self, item_name, mutation, fields):
        self.item_name = item_name
        self.type_spec = get_type_reg().get(u0(self.item_name) + "Form")
        self.mutation = mutation.api_spec
        self.fields = get_fields(self.mutation, fields) if self.mutation else []

    def slug_src(self, field_spec):
        slug_sources = [
            name for name, field_spec in self.fields if field_spec.is_slug_src
        ]
        return R.head(slug_sources) or "Moonleap Todo: slug_src"

    def label(self, name):
        return u0(name.replace(".", " "))

    def display_field_name(self, type_spec):
        return type_spec.display_field.name if type_spec.display_field else "id"
