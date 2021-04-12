from moonleap.render.template_renderer import TemplateRenderer


def render_resources(blocks, settings, output_root_dir):
    template_renderer = TemplateRenderer()
    rendered_resources = []

    for block in blocks:
        for resource in block.get_resources():
            if resource.block is not block:
                continue

            if resource in rendered_resources:
                raise Exception(f"Logical error. Resource in two blocks: {resource}")
            else:
                rendered_resources.append(resource)

            if hasattr(resource, "render"):
                resource.render(
                    settings=settings,
                    output_root_dir=output_root_dir,
                    template_renderer=template_renderer,
                )

    for rendered_resource in list(rendered_resources):
        for _, resource in rendered_resource.get_relations():

            if resource in rendered_resources:
                continue
            else:
                rendered_resources.append(resource)

            if hasattr(resource, "render"):
                resource.render(
                    settings=settings,
                    output_root_dir=output_root_dir,
                    template_renderer=template_renderer,
                )
