from moonleap.utils.queue import Queue
from titan.react_view_pkg.pkg.get_builder import get_builder


def get_helpers(_):
    class Helpers:
        view = _.component
        widget_spec = _.component.widget_spec
        build = None

        def __init__(self):
            self.build = self._get_div(self.widget_spec)

        def _get_div(self, widget_spec, level=0):
            builder = get_builder(widget_spec, None, level)
            builder.build()
            return builder.output

    return Helpers()
