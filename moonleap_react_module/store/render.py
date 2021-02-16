from moonleap.render.template_renderer import render_templates


def render(self, output_root_dir, template_renderer):
    render_templates(__file__)(self, output_root_dir, template_renderer)
