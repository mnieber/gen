from pathlib import Path


def RenderTemplates(root_filename, location="templates"):  # noqa
    from moonleap.render.template_renderer import render_templates
    from moonleap.resource.memfun import MemFun

    class Base:
        if callable(location):
            templates_path = lambda res: Path(root_filename).parent / location(res)
        else:
            templates_path = Path(root_filename).parent / location
        render = MemFun(render_templates(templates_path))

    return Base
