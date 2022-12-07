import copy
import typing as T
import uuid
from dataclasses import dataclass, field

import ramda as R

from .create_widget_class_name import create_widget_class_name


@dataclass
class WidgetSpec:
    widget_base_types: T.List[str] = field(default_factory=list)
    level: int = 0
    child_widget_specs: T.List["WidgetSpec"] = field(repr=False, default_factory=list)
    div_styles: T.List[str] = field(repr=False, default_factory=list)
    div_attrs: T.List[str] = field(repr=False, default_factory=list)
    div_key: T.Optional[str] = None
    props: T.List[str] = field(repr=False, default_factory=list)
    default_props: T.List[str] = field(repr=False, default_factory=list)
    widget_name: T.Optional[str] = None
    module_name: T.Optional[str] = None
    place: T.Optional[str] = None
    values: T.Dict[str, str] = field(default_factory=dict)
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    parent_ws: T.Optional["WidgetSpec"] = None
    # This is the dict from which the widget_spec was created
    src_dict: T.Dict[str, str] = field(default_factory=dict)

    # Private
    _widget_class_name: str = ""

    @property
    def is_component(self):
        return self.widget_name and ":" in self.widget_name

    @property
    def widget_class_name(self):
        if not self._widget_class_name:
            self._widget_class_name = create_widget_class_name(self)
        return self._widget_class_name

    @property
    def is_component_def(self):
        return (
            self.is_component
            and self.widget_base_types
            and self.widget_name not in self.widget_base_types
        )

    def find_child_with_place(self, place):
        return R.head(x for x in self.child_widget_specs if x.place == place)

    def create_memo(self, fields=None):
        fields = fields or ["div_styles", "div_attrs", "div_key", "place", "values"]
        memo = {}
        for field in fields:
            memo[field] = getattr(self, field)
        return copy.deepcopy(memo)

    def restore_memo(self, memo):
        for field, value in memo.items():
            setattr(self, field, value)

    @property
    def root(self):
        ws = self

        while ws.parent_ws and not ws.is_component_def:
            ws = ws.parent_ws

        return ws
