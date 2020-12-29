from moonleap.parser.block import has_terms_in_same_line


def update(block, layer_term, layergroup_term):
    if has_terms_in_same_line(block, layergroup_term, layer_term):
        layer = block.get_resource(layer_term)
        block.get_resource(layergroup_term).layer_by_name.setdefault(layer.name, layer)
        block.drop_resource_by_term(layer_term)
