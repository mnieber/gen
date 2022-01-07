from moonleap import u0
from moonleap.typespec.type_spec_store import type_spec_store
from titan.api_pkg.query.get_default_inputs_type_spec import (
    get_default_inputs_type_spec,
)
from titan.api_pkg.query.get_default_outputs_type_spec import (
    get_default_outputs_type_spec,
)


def inputs_type_spec(self):
    spec_name = f"{u0(self.name)}Input"
    if not type_spec_store().has(spec_name):
        type_spec_store().setdefault(
            spec_name, get_default_inputs_type_spec(self, spec_name)
        )
    return type_spec_store().get(spec_name)


def outputs_type_spec(self):
    spec_name = f"{u0(self.name)}Output"
    if not type_spec_store().has(spec_name):
        type_spec_store().setdefault(
            spec_name, get_default_outputs_type_spec(self, spec_name)
        )
    return type_spec_store().get(spec_name)
