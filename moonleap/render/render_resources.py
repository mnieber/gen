from moonleap.render.template_renderer import TemplateRenderer


def render_resources(blocks, session):
    template_renderer = TemplateRenderer()
    rendered_resources = []

    for block in blocks:
        resources = [x[1] for x in block.get_resource_by_term() if x[2]]
        for resource in resources:
            if resource in rendered_resources:
                raise Exception(f"Logical error. Resource in two blocks: {resource}")

            rendered_resources.append(resource)
            if hasattr(resource, "render"):
                resource.render(
                    settings=session.settings,
                    output_root_dir=session.output_root_dir,
                    template_renderer=template_renderer,
                )

    for rendered_resource in list(rendered_resources):
        resources = [x for _, x in rendered_resource.get_relations()]
        for resource in resources:
            if resource in rendered_resources:
                continue

            rendered_resources.append(resource)
            if hasattr(resource, "render"):
                resource.render(
                    settings=session.settings,
                    output_root_dir=session.output_root_dir,
                    template_renderer=template_renderer,
                )
