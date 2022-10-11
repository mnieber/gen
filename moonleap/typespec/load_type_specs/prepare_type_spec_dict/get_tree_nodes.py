def get_tree_nodes(type_spec_dict, result=None):
    if result is None:
        result = []

    result.append(type_spec_dict)
    for value in type_spec_dict.values():
        if isinstance(value, dict):
            get_tree_nodes(value, result)
    return result


def field_names(node):
    return [x.split()[0] for x in node.keys() if not x.startswith("__")]
