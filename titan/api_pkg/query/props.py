import ramda as R
from moonleap import u0
from moonleap.typespec.field_spec import FieldSpec
from moonleap.typespec.type_spec_store import TypeSpec, type_spec_store
from moonleap.utils.case import camel_join
from moonleap.utils.inflect import plural
from titan.api_pkg.pkg.ml_name import ml_type_spec_from_item_name


def _input_field_spec(field_type, field_name, related_output):
    return FieldSpec(
        name=field_name,
        required=False,
        private=False,
        field_type=field_type,
        field_type_attrs=dict(related_output=related_output),
    )


def _default_inputs_type_spec(self, name):
    input_field_specs = []

    def maybe_create_input_field_specs(src_type_spec, related_output, is_fk):
        query_by = (
            src_type_spec.query_item_by if is_fk else src_type_spec.query_items_by
        )
        for src_field_name in query_by or []:
            input_field_name = camel_join(related_output, src_field_name)
            if not R.head(x for x in input_field_specs if x.name == input_field_name):
                input_field_specs.append(
                    _input_field_spec(
                        src_type_spec.get_field_spec_by_name(src_field_name).field_type,
                        input_field_name,
                        related_output,
                    )
                )

    for named_item_provided in self.named_items_provided:
        item_name, output_field_name = get_output_field_name_for_named_item(
            named_item_provided
        )
        maybe_create_input_field_specs(
            src_type_spec=ml_type_spec_from_item_name(item_name),
            related_output=output_field_name,
            is_fk=True,
        )

    for named_item_list_provided in self.named_item_lists_provided:
        item_name, output_field_name = get_output_field_name_for_named_item_list(
            named_item_list_provided
        )
        maybe_create_input_field_specs(
            src_type_spec=ml_type_spec_from_item_name(item_name),
            related_output=output_field_name,
            is_fk=False,
        )

    return TypeSpec(type_name=name, field_specs=input_field_specs)


def get_output_field_name_for_named_item_list(named_item_list_provided):
    item_name = named_item_list_provided.typ.item_name
    output_field_name = camel_join(named_item_list_provided.name, plural(item_name))
    return item_name, output_field_name


def get_output_field_name_for_named_item(named_item_provided):
    item_name = named_item_provided.typ.item_name
    output_field_name = camel_join(named_item_provided.name, item_name)
    return item_name, output_field_name


def _default_outputs_type_spec(self, name):
    return TypeSpec(
        type_name=name,
        field_specs=[
            *[
                _item_output_field_spec(self, named_item)
                for named_item in self.named_items_provided
            ],
            *[
                _item_list_output_field_spec(self, named_item_list)
                for named_item_list in self.named_item_lists_provided
            ],
        ],
    )


def _item_output_field_spec(self, named_item):
    item_name, output_field_name = get_output_field_name_for_named_item(named_item)
    return FieldSpec(
        name=output_field_name,
        required=False,
        private=False,
        field_type="fk",
        field_type_attrs=dict(
            target=item_name,
            hasRelatedSet=False,
        ),
    )


def _item_list_output_field_spec(self, named_item_list):
    item_name, output_field_name = get_output_field_name_for_named_item_list(
        named_item_list
    )
    return FieldSpec(
        name=output_field_name,
        required=False,
        private=False,
        field_type="relatedSet",
        field_type_attrs=dict(target=item_name),
    )


def inputs_type_spec(self):
    spec_name = f"{u0(self.name)}Input"
    if not type_spec_store().has(spec_name):
        type_spec_store().setdefault(
            spec_name, _default_inputs_type_spec(self, spec_name)
        )
    return type_spec_store().get(spec_name)


def outputs_type_spec(self):
    spec_name = f"{u0(self.name)}Output"
    if not type_spec_store().has(spec_name):
        type_spec_store().setdefault(
            spec_name, _default_outputs_type_spec(self, spec_name)
        )
    return type_spec_store().get(spec_name)
