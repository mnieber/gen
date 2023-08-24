import typing as T

from moonleap import u0

from .strip_fk_symbols import strip_fk_symbols


# This class represents the information in a foreign key that appears in a
# type spec dict.
class ForeignKey:
    def __init__(self, key, value):
        self.maybe_var: T.Optional[str] = None
        self.default_var: T.Optional[str] = None
        self.var_type: T.Optional[str] = None
        self.field_type: T.Optional[str] = None
        self.module_name: T.Optional[str] = None
        self.parts: T.List[str] = []

        self._process_data(
            key, parts=value["__attrs__"].split(",") if "__attrs__" in value else []
        )

    @property
    def var(self):
        return self.maybe_var or self.default_var

    def _process_data(self, value, parts):
        self.parts = list(parts)

        parts_as = value.split(" as ")
        parts_as[-1], more_parts = strip_fk_symbols(parts_as[-1])
        self.parts += more_parts
        parts_module = parts_as[-1].split(".")
        if len(parts_module) > 1:
            self.module_name, parts_as[-1] = parts_module

        if len(parts_as) == 2:
            self.maybe_var, more_parts = strip_fk_symbols(parts_as[0])
            self.parts += more_parts
        else:
            self.default_var = parts_as[-1]

        self.var_type = u0(parts_as[-1])
        if self.var_type.endswith("Set"):
            self.var_type = self.var_type[:-3]
            self.field_type = "relatedSet"
        elif self.var_type.endswith("Form"):
            self.field_type = "form"
        elif self.var_type.endswith("Ids"):
            self.var_type = self.var_type[:-3]
            self.field_type = "uuid[]"
        elif self.var_type.endswith("Id"):
            self.var_type = self.var_type[:-2]
            self.field_type = "uuid"
        else:
            self.field_type = "fk"
