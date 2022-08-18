import typing as T
from dataclasses import dataclass, field

import ramda as R
from moonleap.typespec.field_spec import FieldSpec


@dataclass
class TypeSpec:
    type_name: str
    field_specs: T.List[FieldSpec] = field(repr=False)
    admin_search_by: T.Optional[T.List[str]] = field(default_factory=list)
    display_item_by: T.Optional[str] = None
    select_item_by: T.Optional[T.List[str]] = None
    is_entity: T.Optional[bool] = None
    extract_gql_fields: bool = False
    is_sorted: bool = False

    def get_field_specs(
        self, field_types=None, exclude_names=None, exclude_derived=False
    ):
        return [
            x
            for x in self.field_specs
            if (field_types is None or x.field_type in field_types)
            and x.name not in (exclude_names or [])
            and not (x.derived and exclude_derived)
        ]

    def get_field_spec(self, field_name, derived):
        return R.head(
            x
            for x in self.get_field_specs()
            if x.name == field_name and bool(x.derived) == derived
        )
