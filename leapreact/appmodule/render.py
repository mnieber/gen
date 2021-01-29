from pathlib import Path

from moonleap.render.template_renderer import merged_output_path


def render_module(self, output_root_dir, template_renderer):
    templates_path = Path(__file__).parent / "templates"
    output_path = merged_output_path(self.output_paths.merged)
    output_sub_dir = output_path.location

    template_paths = (
        templates_path.glob("*") if templates_path.is_dir() else [templates_path]
    )
    for template_fn in template_paths:
        if not template_fn.is_dir():
            template_renderer.render(output_root_dir, output_sub_dir, self, template_fn)
