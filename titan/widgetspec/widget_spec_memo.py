import copy


# A Context class that calls create_memo and restore_memo on the widget_spec
# when entering and exiting a context.
class WidgetSpecMemoContext:
    def __init__(self, widget_spec, fields):
        self.widget_spec = widget_spec
        self.fields = fields
        self.memo = None

    def __enter__(self):
        self.memo = _create_memo(self.widget_spec, self.fields)
        return self.widget_spec

    def __exit__(self, exc_type, exc_value, traceback):
        _restore_memo(self.widget_spec, self.memo)
        self.memo = None


def _create_memo(widget_spec, fields):
    memo = {}
    for field in fields:
        memo[field] = getattr(widget_spec, field)
    return copy.deepcopy(memo)


def _restore_memo(widget_spec, memo):
    for field, value in memo.items():
        setattr(widget_spec, field, value)
