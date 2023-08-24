import typing as T
from dataclasses import dataclass, field


@dataclass
class FieldSpec:
    field_type: str
    key: str

    admin_search: bool = field(default=False, repr=False)
    admin: bool = field(default=True, repr=False)
    choices: T.Optional[T.List[T.Any]] = field(default=None, repr=False)
    default_value: T.Any = field(default=None, repr=False)
    description: T.Optional[str] = field(default=None, repr=False)
    display: T.Optional[bool] = field(default=None, repr=False)
    has_api: T.Optional[bool] = field(default=None)
    has_model: T.Optional[bool] = field(default=True)
    help: T.Optional[bool] = field(default=None, repr=False)
    index: T.Optional[bool] = field(default=None, repr=False)
    is_inverse: T.Optional[bool] = field(default=None)
    is_optional: T.Optional[bool] = field(default=None)
    is_slug_src: T.Optional[bool] = field(default=None, repr=False)
    max_length: T.Optional[int] = field(default=None, repr=False)
    primary_key: T.Optional[bool] = field(default=None, repr=False)
    readonly: T.Optional[bool] = field(default=None, repr=False)
    target: T.Optional[str] = None
    unique: T.Optional[bool] = field(default=None, repr=False)

    @property
    def name(self):
        return self.key.rstrip("~")


@dataclass
class FormFieldSpec(FieldSpec):
    pass


@dataclass
class FkFieldSpec(FieldSpec):
    related_name: T.Optional[str] = None
    admin_inline: T.Optional[bool] = field(default=None, repr=False)
    set_null: T.Optional[bool] = field(default=None, repr=False)


def get_field_spec_constructor(t):
    return (
        FkFieldSpec
        if t in ("fk", "relatedSet")
        else FormFieldSpec
        if t in ("form",)
        else FieldSpec
    )
