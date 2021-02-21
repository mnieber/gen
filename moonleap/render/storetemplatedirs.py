from moonleap import MemField, MemFun
from moonleap.render.template_renderer import render_templates


def render(self, output_root_dir, template_renderer):
    for root_filename, location in self.template_dirs:
        render_templates(root_filename, location)(
            self, output_root_dir, template_renderer
        )


def add_template_dir(self, root_filename, location):
    new_template_dir = (root_filename, location)
    if new_template_dir not in self.template_dirs:
        self.template_dirs.append(new_template_dir)


class StoreTemplateDirs:
    template_dirs = MemField(lambda: list())
    render = MemFun(render)
    add_template_dir = MemFun(add_template_dir)
