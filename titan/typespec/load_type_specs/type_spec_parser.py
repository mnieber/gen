import typing as T

from moonleap import is_private_key, l0, u0
from titan.types_pkg.pkg.form_type_spec_from_data_type_spec import (
    form_type_spec_from_data_type_spec,
)
from titan.typespec.load_type_specs.add_type_spec_to_type_reg import (
    add_type_spec_to_type_reg,
)
from titan.typespec.load_type_specs.process_api_spec import process_api_spec
from titan.typespec.load_type_specs.process_form_spec import process_form_spec
from titan.typespec.load_type_specs.set_related_name import set_related_name
from titan.typespec.type_spec import TypeSpec

from .add_extra_model_fields import add_extra_model_fields
from .add_field_spec import add_field_spec
from .create_type_spec import create_type_spec
from .field_spec_from_dict import field_spec_from_dict, is_pass
from .foreign_key import ForeignKey


class TypeSpecParser:
    def __init__(self, type_reg):
        self.type_reg = type_reg

    def parse(self, type_spec_dict, parent_type_spec=None):
        # For debugging purposes, we create a new dict that shows how the parser
        # interprets and modifies the type_spec_dict.
        trace = dict()

        # Stores the keys that we add to parent_type_spec in this iteration.
        keys = []

        items = [
            (key.strip(), value)
            for key, value in type_spec_dict.items()
            if not is_private_key(key)
        ]

        scalar_items = [item for item in items if not _is_fk_item(item)]
        fk_items = [item for item in items if _is_fk_item(item)]

        if scalar_items and not parent_type_spec:
            raise Exception("The root type spec dict cannot contain scalar fields")

        for key, value in scalar_items:
            # Get field spec and related data from key/value pair
            field_spec_data = field_spec_from_dict(key, value)
            field_spec = field_spec_data["field_spec"]
            trace[field_spec_data["new_key"]] = field_spec_data["new_value"]

            # Add field spec to type spec
            if parent_type_spec:
                add_field_spec(parent_type_spec, field_spec)
                keys.append(field_spec.key)

        while fk_items:
            key, value = fk_items.pop(0)

            # Get field spec and related data from key/value pair
            field_spec_data = field_spec_from_dict(key, value)
            org_value, value = value, T.cast(T.Dict, field_spec_data["new_value"])
            is_pass = field_spec_data["is_pass"]
            fk = T.cast(ForeignKey, field_spec_data["fk"])
            field_spec = field_spec_data["field_spec"]

            # Add field spec to type spec
            if parent_type_spec:
                add_field_spec(parent_type_spec, field_spec)
                keys.append(field_spec.key)

            # Get/update the target type
            if field_spec.field_type in ("fk", "relatedSet", "form"):
                fk_type_spec = create_type_spec(
                    fk.var_type,
                    (u0(value["__base_type__"]) if "__base_type__" in value else None),
                    fk.parts,
                    module_name=(value.get("__module__") or fk.module_name),
                )

                add_extra_model_fields(fk_type_spec, value)

                #
                # Use recursion to convert child type specs
                #
                fk_trace, fk_keys = self.parse(value, parent_type_spec=fk_type_spec)

                # Set related name.
                if parent_type_spec and field_spec.field_type in ("fk", "relatedSet"):
                    set_related_name(
                        field_spec=field_spec, type_spec=fk_type_spec, keys=fk_keys
                    )

                add_type_spec_to_type_reg(
                    self.type_reg,
                    fk_type_spec,
                    parent_type_spec=parent_type_spec,
                )

                # Update trace
                if fk.parts:
                    fk_trace["__attrs__"] = ",".join(fk.parts)
                trace[_trace_key(fk)] = org_value if is_pass else fk_trace

                # If there is an api spec then we create a related api-type_spec and
                # use it to update fk_type_spec.
                api_spec = value.get("__api__")
                if api_spec:
                    api_type_spec = TypeSpec(
                        type_name=fk_type_spec.type_name + "Api", field_specs=[]
                    )
                    self.parse(api_spec, parent_type_spec=api_type_spec)
                    process_api_spec(fk_type_spec, api_spec, api_type_spec)

                # If there is an form type spec then we create a related form-type_spec.
                # If there is an existing form-type_spec then we update it.
                form_spec = value.get("__form__")
                if form_spec:
                    form_type_spec_name = fk_type_spec.type_name + "Form"
                    form_type_spec = form_type_spec_from_data_type_spec(
                        fk_type_spec,
                        form_type_spec_name,
                        form_spec.get("__delete__", []),
                    )
                    self.parse(form_spec, parent_type_spec=form_type_spec)
                    form_type_spec.module_name = self.type_reg.get(
                        fk_type_spec.type_name
                    ).module_name
                    process_form_spec(self.type_reg, form_type_spec)

        return trace, keys


def _is_fk_item(item):
    return isinstance(item[1], dict) or is_pass(item[1])


def _trace_key(fk):
    suffix = (
        "Set"
        if fk.field_type == "relatedSet"
        else "Form"
        if fk.field_type == "form"
        else "Id"
        if fk.field_type == "id"
        else "Ids"
        if fk.field_type == "uuid[]"
        else ""
    )
    return (
        f"{fk.maybe_var} as {l0(fk.var_type)}{suffix}"
        if fk.maybe_var
        else fk.default_var
    )
