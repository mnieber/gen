from moonleap.render.add_output_filenames import add_output_filenames
from moonleap.render.template_renderer import render_templates


def render(self, output_root_dir, template_renderer):
    all_output_filenames = []

    for module in self.service.django_app.modules:
        if module.item_types or module.forms:
            add_output_filenames(
                all_output_filenames,
                render_templates(__file__, "templates_module")(
                    module, output_root_dir, template_renderer
                ),
            )
    return all_output_filenames
