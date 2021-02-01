from pathlib import Path

from moonleap.render.template_renderer import merged_output_path, render_templates


def render_module(self, output_root_dir, template_renderer):
    render_templates(__file__)(self, output_root_dir, template_renderer)

    # render index.tsx into the parent dir of merged_output_path(self)
    render_templates(
        __file__, "templates_index", output_subdir=merged_output_path(self).parent
    )(self, output_root_dir, template_renderer)
