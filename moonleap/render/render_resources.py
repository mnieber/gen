from moonleap.render.render_template import render_template


def render_resources(blocks, write_file):
    rendered_resources = []

    try:
        for block in blocks:
            resources = [x[1] for x in block.get_resource_by_term() if x[2]]
            for resource in resources:
                if resource in rendered_resources:
                    raise Exception(
                        f"Logical error. Resource in two blocks: {resource}"
                    )

                rendered_resources.append(resource)
                if hasattr(resource, "render"):
                    resource.render(
                        write_file=write_file,
                        render_template=render_template,
                        output_path=resource.merged_output_path,
                    )

        for rendered_resource in list(rendered_resources):
            resources = [x for _, x in rendered_resource.get_relations()]
            for resource in resources:
                if resource in rendered_resources:
                    continue

                rendered_resources.append(resource)
                if hasattr(resource, "render"):
                    resource.render(
                        write_file=write_file,
                        render_template=render_template,
                        output_path=resource.merged_output_path,
                    )

    except Exception:
        raise
