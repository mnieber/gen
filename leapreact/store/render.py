from pathlib import Path

from moonleap.render.template_renderer import merged_output_path, render_templates


def render(self, output_root_dir, template_renderer):
    render_templates(__file__)(self, output_root_dir, template_renderer)
