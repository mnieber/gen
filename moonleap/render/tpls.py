from moonleap.render.render_template import render_template


class Tpls:
    def __init__(self, base_name, **tpls):
        self.base_name = base_name
        self.tpls = tpls

    def render(self, tpl_name, context):
        return render_template(
            self.base_name + "_" + tpl_name + ".j2", context, self.tpls[tpl_name]
        )
