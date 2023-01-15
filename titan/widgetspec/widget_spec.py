import typing as T
import uuid
from dataclasses import dataclass, field

import ramda as R

from titan.widgetspec.create_widget_class_name import create_widget_class_name
from titan.widgetspec.div import Div
from titan.widgetspec.widget_spec_memo import WidgetSpecMemoContext


@dataclass
class WidgetSpec:
    widget_base_types: T.List[str] = field(default_factory=list)
    child_widget_specs: T.List["WidgetSpec"] = field(repr=False, default_factory=list)
    div: Div = field(default_factory=Div)
    widget_name: T.Optional[str] = None
    module_name: T.Optional[str] = None
    place: T.Optional[str] = None
    place_values: T.Dict[str, str] = field(default_factory=dict)
    values: T.Dict[str, str] = field(default_factory=dict)
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    parent: T.Optional["WidgetSpec"] = field(repr=False, default=None)
    # This is the dict from which the widget_spec was created
    src_dict: T.Dict[str, str] = field(default_factory=dict)

    # Private
    _widget_class_name: str = ""

    @property
    def is_component(self):
        return self.widget_name and ":" in self.widget_name

    @property
    def is_component_def(self):
        return bool(
            self.is_component
            and self.widget_base_types
            and self.widget_name not in self.widget_base_types
        )

    @property
    def widget_class_name(self):
        if not self._widget_class_name:
            self._widget_class_name = create_widget_class_name(self)
        return self._widget_class_name

    def set_widget_class_name(self, value):
        self._widget_class_name = value

    def get_place(self, place):
        return R.head(x for x in self.child_widget_specs if x.place == place)

    def memo(self, fields=None):
        return WidgetSpecMemoContext(self, fields)

    def get_value_by_name(self, name, default=None):
        ws = self
        while ws:
            value = ws.values.get(name)
            if value:
                return value
            ws = ws.parent
        return default

    @property
    def root(self):
        ws = self
        while ws.parent and not ws.is_component_def:
            ws = ws.parent
        return ws
