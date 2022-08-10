from moonleap.render.render_templates import render_templates
from moonleap.resource.memfield import MemField
from moonleap.resource.memfun import MemFun


def render(self, write_file, render_template, output_path):
    for template_dir, get_context, skip_render in self.template_dirs:
        if skip_render and skip_render(self):
            continue
        render_templates(
            template_dir, self, write_file, render_template, output_path, get_context
        )


def add_template_dir(self, template_dir, get_context=None, skip_render=None):
    if not [x for x in self.template_dirs if x[0] == template_dir]:
        self.template_dirs.append((template_dir, get_context, skip_render))


class StoreTemplateDirs:
    template_dirs = MemField(lambda: list())
    render = MemFun(render)
    add_template_dir = MemFun(add_template_dir)
