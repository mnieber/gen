import typing as T
from dataclasses import dataclass, field

import ramda as R


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

    def remove_child_with_place(self, place):
        widget_spec = R.head(
            x for x in self.child_widget_specs if x.place == "ListViewItem"
        )
        if widget_spec:
            self.child_widget_specs.remove(widget_spec)
