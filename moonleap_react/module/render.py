from moonleap.render.template_renderer import render_templates


def render(self, output_root_dir, template_renderer):
    for root_filename, location in self.template_dirs:
        render_templates(root_filename, location)(
            self, output_root_dir, template_renderer
        )
