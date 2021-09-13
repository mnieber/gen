from moonleap import MemField, MemFun
from moonleap.render.template_renderer import render_templates


def render(self, write_file, render_template):
    for template_dir in self.template_dirs:
        render_templates(template_dir)(self, write_file, render_template)


def add_template_dir(self, template_dir):
    if template_dir not in self.template_dirs:
        self.template_dirs.append(template_dir)


class StoreTemplateDirs:
    template_dirs = MemField(lambda: list())
    render = MemFun(render)
    add_template_dir = MemFun(add_template_dir)
