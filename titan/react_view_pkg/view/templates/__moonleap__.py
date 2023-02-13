from titan.widgetspec.get_scss_styles_by_class_name import get_scss_styles_by_class_name


def get_helpers(_):
    class Helpers:
        view = _.component
        widget_spec = _.component.widget_spec
        build = view.build_output
        pipelines = widget_spec.pipelines
        has_children_prop = widget_spec.has_tag("has_children_prop")
        has_scss = not widget_spec.has_tag("no_scss")
        has_default_props = bool(build.default_props) or not widget_spec.get_value(
            "noDps"
        )
        has_click_handler = "click:handler" in widget_spec.handler_term_strs

        def __init__(self):
            (
                self.scss_imports,
                self.scss_styles_by_class_name,
            ) = get_scss_styles_by_class_name(self.widget_spec)

    return Helpers()
