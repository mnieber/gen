import os

from moonleap.render.template_env import template_env
from moonleap.render.transforms import post_transforms


def render_template(resource, template_fn, **kwargs):
    if template_fn.suffix == ".j2":
        template = template_env.get_template(str(template_fn))
        content = template.render(res=resource, **kwargs)

        lines = content.split(os.linesep)
        for post_transform in post_transforms:
            lines = post_transform(lines)
        content = os.linesep.join(lines)
    else:
        with open(template_fn) as ifs:
            content = ifs.read()

    return content


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
                    )

    except Exception:
        raise
