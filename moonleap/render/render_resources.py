from moonleap.render.add_output_filenames import add_output_filenames
from moonleap.render.post_process_output_files import post_process_output_files
from moonleap.render.template_renderer import TemplateRenderer
from moonleap.session import get_session


def render_resources(blocks):
    session = get_session()
    session.report("Rendering...")
    all_output_filenames = _render_resources(blocks, session)
    session.report("Post processing...")
    post_process_output_files(
        all_output_filenames,
        session.settings.get("post_process", {}),
        session.settings.get("bin", {}),
    )


def _render_resources(blocks, session):
    template_renderer = TemplateRenderer()
    rendered_resources = []
    all_output_filenames = []

    for block in blocks:
        resources = [x[1] for x in block.get_resource_by_term() if x[2]]
        for resource in resources:
            if resource in rendered_resources:
                raise Exception(f"Logical error. Resource in two blocks: {resource}")

            rendered_resources.append(resource)
            if hasattr(resource, "render"):
                add_output_filenames(
                    all_output_filenames,
                    resource.render(
                        output_root_dir=session.output_root_dir,
                        template_renderer=template_renderer,
                    ),
                )

    for rendered_resource in list(rendered_resources):
        resources = [x for _, x in rendered_resource.get_relations()]
        for resource in resources:
            if resource in rendered_resources:
                continue

            rendered_resources.append(resource)
            if hasattr(resource, "render"):
                add_output_filenames(
                    all_output_filenames,
                    resource.render(
                        output_root_dir=session.output_root_dir,
                        template_renderer=template_renderer,
                    ),
                )

    return all_output_filenames
