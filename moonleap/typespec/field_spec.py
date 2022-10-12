import typing as T
from dataclasses import dataclass, field


@dataclass
class FieldSpec:
    field_type: str
    key: str
    admin_search: bool = field(default=False, repr=False)
    admin: bool = field(default=True, repr=False)
    has_api: T.List[str] = field(default_factory=lambda: [])
    has_model: T.List[str] = field(default_factory=lambda: [])
    choices: T.Optional[T.List[T.Any]] = field(default=None, repr=False)
    default_value: T.Any = field(default=None, repr=False)
    description: T.Optional[str] = field(default=None, repr=False)
    display: T.Optional[bool] = field(default=None, repr=False)
    help: T.Optional[bool] = field(default=None, repr=False)
    index: T.Optional[bool] = field(default=None, repr=False)
    is_slug_src: T.Optional[bool] = field(default=None, repr=False)
    max_length: T.Optional[int] = field(default=None, repr=False)
    primary_key: T.Optional[bool] = field(default=None, repr=False)
    readonly: T.Optional[bool] = field(default=None, repr=False)
    is_auto: T.Optional[bool] = field(default=None)
    # If "server" in optional, then the field is optional on the server.
    # Sometimes, a field is labelled explicitly as required by adding "required_server" to optional.
    # This is used when the default is optional by default (e.g. in a many-to-many relationship).
    optional: T.List[str] = field(default_factory=lambda: [])
    target: T.Optional[str] = None
    readonly: T.Optional[bool] = field(default=None, repr=False)
    unique: T.Optional[bool] = field(default=None, repr=False)

    @property
    def name(self):
        return self.key.removesuffix("~")


@dataclass
class FormFieldSpec(FieldSpec):
    pass


@dataclass
class FkFieldSpec(FieldSpec):
    through: T.Optional[str] = None
    through_var: T.Optional[str] = None
    related_name: T.Optional[str] = None
    admin_inline: T.Optional[bool] = None
    set_null: T.Optional[bool] = None


def get_field_spec_constructor(t):
    return (
        FkFieldSpec
        if t in ("fk", "relatedSet")
        else FormFieldSpec
        if t in ("form",)
        else FieldSpec
    )
