import typing as T
from dataclasses import dataclass, field


@dataclass
class WidgetSpec:
    widget_base_type: str
    child_widget_specs: T.List["WidgetSpec"] = field(repr=False, default_factory=list)
    styles: T.List[str] = field(repr=False, default_factory=list)
    widget_type: T.Optional[str] = None
    module_name: T.Optional[str] = None
    place: T.Optional[str] = None
    values: T.Dict[str, str] = field(repr=False, default_factory=dict)

    @property
    def is_component(self):
        return self.widget_type and ":" in self.widget_type
