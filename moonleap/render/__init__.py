def RenderTemplates(root_filename, location="templates"):  # noqa
    from moonleap.render.template_renderer import render_templates
    from moonleap.resource.memfun import MemFun

    class Base:
        render = MemFun(render_templates(root_filename, location))

    return Base
