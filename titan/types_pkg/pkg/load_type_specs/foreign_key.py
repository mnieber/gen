import typing as T
from dataclasses import dataclass, field

from moonleap.utils.case import l0, u0

from .strip_fk_symbols import strip_fk_symbols


@dataclass
class Data:
    var: T.Optional[str] = None
    default_var: T.Optional[str] = None
    var_type: T.Optional[str] = None
    field_type: T.Optional[str] = None
    module_name: T.Optional[str] = None
    parts: T.List[str] = field(default_factory=list)
    related_name: T.Optional[str] = None

    @property
    def key(self):
        suffix = (
            "Set"
            if self.field_type == "relatedSet"
            else "Form"
            if self.field_type == "form"
            else "Id"
            if self.field_type == "id"
            else "Ids"
            if self.field_type == "uuid[]"
            else ""
        )
        return (
            f"{self.var} as {l0(self.var_type)}{suffix}"
            if self.var
            else self.default_var
        )


# This class represents the information in a foreign key that appears in a
# type spec dict.
class ForeignKey:
    def __init__(self, key, value):
        _init_parts = value["__type__"].split(".") if "__type__" in value else []
        _init_target_parts = (
            value["__target_type__"].split(".") if "__target_type__" in value else []
        )
        parts_through = key.split(" through ")
        if len(parts_through) == 2:
            self.foo, self.bar = Data(), Data()
            _process_data(self.foo, parts_through[0], _init_target_parts)
            _process_data(self.bar, parts_through[1], _init_parts)
        else:
            self.foo, self.bar = Data(), None
            _process_data(self.foo, key, _init_parts)

    @property
    def data(self):
        return self.bar or self.foo

    @property
    def data_parts(self):
        return self.data.parts

    @property
    def target_parts(self):
        return [] if not self.bar else self.foo.parts

    @property
    def var(self):
        return self.foo.var or self.foo.default_var

    @property
    def var_type(self):
        return self.foo.var_type

    @property
    def through_var(self):
        return self.bar.var or self.bar.default_var

    @property
    def through_var_type(self):
        return f"{l0(self.bar.var_type)}Set"

    @property
    def clean_key(self):
        return self.foo.key + ((" through " + self.bar.key) if self.bar else "")


def _process_data(data, value, parts):
    data.parts = list(parts)

    parts_with = value.split(" with ")
    if len(parts_with) == 2:
        data.related_name = parts_with[1]
        value = parts_with[0]

    parts_as = value.split(" as ")
    parts_as[-1], more_parts = strip_fk_symbols(parts_as[-1])
    data.parts += more_parts
    parts_module = parts_as[-1].split(".")
    if len(parts_module) > 1:
        data.module_name, parts_as[-1] = parts_module

    if len(parts_as) == 2:
        data.var, more_parts = strip_fk_symbols(parts_as[0])
        data.parts += more_parts
    else:
        data.default_var = parts_as[-1]

    data.var_type = u0(parts_as[-1])
    if data.var_type.endswith("Set"):
        data.var_type = data.var_type[:-3]
        data.field_type = "relatedSet"
    elif data.var_type.endswith("Form"):
        data.field_type = "form"
    elif data.var_type.endswith("Ids"):
        data.var_type = data.var_type[:-3]
        data.field_type = "uuid[]"
    elif data.var_type.endswith("Id"):
        data.var_type = data.var_type[:-2]
        data.field_type = "uuid"
    else:
        data.field_type = "fk"
