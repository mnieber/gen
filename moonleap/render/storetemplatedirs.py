from moonleap import MemField, MemFun
from moonleap.render.add_output_filenames import add_output_filenames
from moonleap.render.template_renderer import render_templates


def render(self, output_root_dir, template_renderer):
    all_output_filenames = []

    for root_filename, location in self.template_dirs:
        add_output_filenames(
            all_output_filenames,
            render_templates(root_filename, location)(
                self, output_root_dir, template_renderer
            ),
        )
    return all_output_filenames


def add_template_dir(self, root_filename, location):
    new_template_dir = (root_filename, location)
    if new_template_dir not in self.template_dirs:
        self.template_dirs.append(new_template_dir)


class StoreTemplateDirs:
    template_dirs = MemField(lambda: list())
    render = MemFun(render)
    add_template_dir = MemFun(add_template_dir)
