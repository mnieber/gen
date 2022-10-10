import typing as T
from dataclasses import dataclass, field


@dataclass
class FieldSpec:
    field_type: str
    name: str
    admin_search: bool = False
    admin: bool = True
    api: T.List[str] = field(default_factory=lambda: ["server", "client"])
    choices: T.Optional[T.List[T.Any]] = None
    default_value: T.Any = None
    derived: T.Optional[bool] = None
    description: T.Optional[str] = None
    display: T.Optional[bool] = None
    help: T.Optional[bool] = None
    index: T.Optional[bool] = None
    is_slug_src: T.Optional[bool] = None
    max_length: T.Optional[int] = None
    primary_key: T.Optional[bool] = None
    readonly: T.Optional[bool] = None
    required: T.Optional[bool] = None
    target: T.Optional[str] = None
    readonly: T.Optional[bool] = None
    unique: T.Optional[bool] = None


@dataclass
class FormFieldSpec(FieldSpec):
    pass


@dataclass
class FkFieldSpec(FieldSpec):
    through: T.Optional[str] = None
    through_as: T.Optional[str] = None
    is_parent_of_target: T.Optional[bool] = None
    is_parent_of_through: T.Optional[bool] = None
    is_reverse_of_related_set: T.Optional["FkFieldSpec"] = None
    admin_inline: T.Optional[bool] = None
    set_null: T.Optional[bool] = None


def get_field_spec_constructor(t):
    return (
        FkFieldSpec
        if t in ("fk", "relatedSet")
        else FormFieldSpec
        if t in ("form")
        else FieldSpec
    )
