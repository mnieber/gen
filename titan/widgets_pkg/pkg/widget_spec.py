import typing as T
from dataclasses import dataclass, field


@dataclass
class WidgetSpec:
    widget_type: str
    child_widget_specs: T.List["WidgetSpec"] = field(repr=False, default_factory=list)
    styles: T.List[str] = field(repr=False, default_factory=list)
    widget_name: T.Optional[str] = None
    module_name: T.Optional[str] = None
    values: T.List[str] = field(repr=False, default_factory=list)

    @property
    def is_component(self):
        return self.widget_name and self.widget_name[0].isupper()


def get_widget_spec_constructor(widget_type):
    return WidgetSpec
