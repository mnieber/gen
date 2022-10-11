from moonleap.utils.fp import add_to_list_as_set

from .get_tree_nodes import field_names, get_tree_nodes


def add_missing_entity_fields(type_spec_dict):
    tree_nodes = get_tree_nodes(type_spec_dict)
    entities = []

    for node in tree_nodes:
        if _is_entity_node(node):
            add_to_list_as_set(entities, node.get("__type_name__"))

    for node in tree_nodes:
        if _is_entity_node(node) and "id" in field_names(node):
            entities.remove(node.get("__type_name__"))

    for node in tree_nodes:
        if _is_entity_node(node) and node.get("__type_name__") in entities:
            node["id"] = "Id.primary_key.client_api"
            entities.remove(node.get("__type_name__"))


def _is_entity_node(node):
    init = node.get("__init__")
    return init and "entity" in init.split(".")
