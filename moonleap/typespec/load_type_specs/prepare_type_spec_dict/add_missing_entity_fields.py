from moonleap.utils.fp import add_to_list_as_set


def add_missing_entity_fields(type_spec_dict):
    tree_nodes = _get_tree_nodes(type_spec_dict)
    entities = []

    for node in tree_nodes:
        if _is_entity_node(node):
            add_to_list_as_set(entities, node.get("__type_name__"))

    for node in tree_nodes:
        if _is_entity_node(node) and "id" in _field_names(node):
            entities.remove(node.get("__type_name__"))

    for node in tree_nodes:
        if _is_entity_node(node) and node.get("__type_name__") in entities:
            node["id"] = "Id.primary_key.client_api"
            entities.remove(node.get("__type_name__"))


def _get_tree_nodes(type_spec_dict, result=None):
    if result is None:
        result = []

    result.append(type_spec_dict)
    for value in type_spec_dict.values():
        if isinstance(value, dict):
            _get_tree_nodes(value, result)
    return result


def _field_names(node):
    return [x.split()[0] for x in node.keys() if not x.startswith("__")]


def _is_entity_node(node):
    init_key = "__init_target__" if "__init_target__" in node else "__init__"
    init = node.get(init_key)
    return init and "entity" in init.split(".")
