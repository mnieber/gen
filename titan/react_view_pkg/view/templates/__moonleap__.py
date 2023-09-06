from moonleap.utils.indent import indent


def get_helpers(_):
    class Helpers:
        view = _.component

        def __init__(self):
            pass

        def render_main_div(self):
            return indent(6)(tpl.replace("MyComponent", self.view.name))

    return Helpers()


tpl = """/*
🔳 MyComponent 🔳
*/
<div className={cn('MyComponent', 'yes!', props.className)}>
</div>
"""
