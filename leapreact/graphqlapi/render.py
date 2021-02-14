from pathlib import Path

from moonleap.render.template_renderer import merged_output_path, render_templates


def render(self, output_root_dir, template_renderer):
    render_templates(__file__)(self, output_root_dir, template_renderer)

    # render templates_app into the app directory
    __import__("pudb").set_trace()
    app_module = self.module.service.app_module
    render_templates(
        __file__, "templates_app", output_subdir=merged_output_path(app_module)
    )(self, output_root_dir, template_renderer)
