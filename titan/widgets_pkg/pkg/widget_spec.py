import copy
import typing as T
import uuid
from dataclasses import dataclass, field

import ramda as R

from .create_widget_class_name import create_widget_class_name


@dataclass
class WidgetSpec:
    widget_base_type: str
    level: int = 0
    child_widget_specs: T.List["WidgetSpec"] = field(repr=False, default_factory=list)
    div_styles: T.List[str] = field(repr=False, default_factory=list)
    div_props: T.List[str] = field(repr=False, default_factory=list)
    div_key: T.Optional[str] = None
    widget_name: T.Optional[str] = None
    module_name: T.Optional[str] = None
    place: T.Optional[str] = None
    values: T.Dict[str, str] = field(default_factory=dict)
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    parent: T.Optional["WidgetSpec"] = None

    @property
    def is_component(self):
        return self.widget_name and ":" in self.widget_name

    @property
    def widget_class_name(self):
        return create_widget_class_name(self)

    @property
    def is_component_def(self):
        return (
            self.is_component
            and self.widget_base_type
            and self.widget_base_type != self.widget_name
        )

    def find_child_with_place(self, place):
        return R.head(x for x in self.child_widget_specs if x.place == place)

    def create_memo(self, fields=None):
        fields = fields or ["div_styles", "div_props", "div_key", "place", "values"]
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

        while ws.parent and not ws.is_component_def:
            ws = ws.parent

        return ws
