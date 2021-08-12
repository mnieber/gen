from moonleap.resources.data_type_spec_store import data_type_spec_store


def p_section_item_fields(self, item_name):
    spec = data_type_spec_store.get_spec(item_name)
    return "\n".join([f"    {x.name}: null," for x in spec.fields if x.name != "id"])
