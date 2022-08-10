from titan.api_pkg.typeregistry import get_type_reg


def get_helpers(_):
    class Helpers:
        type_reg = get_type_reg()
        item_list = _.item_type.item.item_list
        type_spec = _.item_type.type_spec
        private_field_specs = [x for x in type_spec.field_specs if x.private]
        form_field_specs = (
            [x for x in _.item_type.form_type.type_spec.field_specs if not x.private]
            if _.item_type.form_type
            else []
        )

    return Helpers()
