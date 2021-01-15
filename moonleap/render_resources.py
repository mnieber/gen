from moonleap.render.template_renderer import TemplateRenderer


def render_resources(blocks, output_root_dir):
    template_renderer = TemplateRenderer(output_root_dir)

    for block in blocks:
        for resource in block.get_entities():
            if resource.block is not block:
                continue

            if hasattr(resource, "render"):
                resource.render(template_renderer)
