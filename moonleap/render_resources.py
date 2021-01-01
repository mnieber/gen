from moonleap.config import config


def render_resources(blocks, root_dir):
    for block in blocks:
        for resource in block.get_resources():
            render = config.render_function_by_resource_type_id.get(resource.type_id)
            if render:
                render(resource, root_dir)
