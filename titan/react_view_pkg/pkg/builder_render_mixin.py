from moonleap.render.render_template import render_template


class BuilderRenderMixin:
    def __init__(self):
        self.template_dir = None

    def render(self, template, context):
        return render_template(self.template_dir / template, context)

    def render_str(self, template_str, context, template_id):
        assert template_id.endswith(".j2")
        return render_template(template_id, context, template_str)
