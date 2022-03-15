import typing as T
from dataclasses import dataclass, field

from moonleap import Resource
from moonleap.utils.case import l0, sn

from .utils import _on_delete


@dataclass
class DjangoModelField(Resource):
    name: str
    field_name: str
    index: bool = False
    required: T.Optional[bool] = None
    unique: T.Optional[bool] = None
    help_text: T.Optional[str] = None

    def field_args(self):
        return []

    def arg_null_blank(self):
        return [] if self.required else ["null=True", "blank=True"]

    def arg_unique(self):
        return ["unique=True"] if self.unique else []

    def arg_help_text(self):
        return [f'help_text="{self.help_text}"'] if self.help_text else []

    def arg_default(self):
        return []

    @property
    def body(self):
        args = [x for x in self.field_args() if x is not None] + [
            *self.arg_default(),
            *self.arg_null_blank(),
            *self.arg_unique(),
            *self.arg_help_text(),
        ]
        args_str = ", ".join(args)
        if args_str.startswith(","):
            __import__("pudb").set_trace()
        return f"models.{self.field_name}({args_str})"


@dataclass
class DjangoFkField(DjangoModelField):
    target: str = ""
    admin_inline: bool = False
    related_name: str = "+"
    on_delete: str = "models.SET_NULL"
    field_name: str = "ForeignKey"

    def field_args(self):
        return [
            self.target,
            f"on_delete={self.on_delete}",
            f'related_name="{self.related_name}"',
        ]


@dataclass
class DjangoManyToManyField(DjangoModelField):
    target: str = ""
    admin_inline: bool = False
    through: str = "+"
    related_name: str = "+"
    field_name: str = "ManyToManyField"

    def arg_null_blank(self):
        return [] if self.required else ["blank=True"]

    def field_args(self):
        return [
            self.target,
            None if self.through == "+" else f'through="{self.through}"',
            f'related_name="{self.related_name}"',
        ]


@dataclass
class DjangoCharField(DjangoModelField):
    max_length: int = 80
    default: T.Optional[str] = None
    choices: T.List[str] = field(default_factory=list)
    field_name: str = "CharField"

    def arg_default(self):
        return [f'default="{self.default}"'] if self.default else []

    def field_args(self):
        choice_items = [f'("{x}", "{x}")' for x in self.choices or []]
        choices_arg = f"choices=[{', '.join(choice_items)}]" if choice_items else None
        return [
            f"max_length={self.max_length}",
            choices_arg,
        ]


@dataclass
class DjangoTextField(DjangoModelField):
    default: T.Optional[str] = None
    field_name: str = "TextField"

    def arg_default(self):
        return [f'default="{self.default}"'] if self.default else []


@dataclass
class DjangoJsonField(DjangoModelField):
    default: T.Optional[str] = None
    field_name: str = "JSONField"

    def arg_default(self):
        return [f'default="{self.default}"'] if self.default else []


@dataclass
class DjangoSlugField(DjangoModelField):
    max_length: int = 80
    slug_src: T.Optional[str] = None
    field_name: str = "SlugField"

    def field_args(self):
        return [f"max_length={self.max_length}"]


@dataclass
class DjangoUrlField(DjangoModelField):
    max_length: int = 80
    default: T.Optional[str] = None
    field_name: str = "URLField"

    def arg_default(self):
        return [f'default="{self.default}"'] if self.default else []

    def field_args(self):
        return [f"max_length={self.max_length}"]


@dataclass
class DjangoBooleanField(DjangoModelField):
    default: T.Optional[bool] = None
    field_name: str = "BooleanField"

    def arg_default(self):
        return (
            [f'default={"True" if self.default else "False"}']
            if self.default in (True, False)
            else []
        )


@dataclass
class DjangoIntegerField(DjangoModelField):
    default: T.Optional[int] = None
    field_name: str = "IntegerField"

    def arg_default(self):
        return [f"default={self.default}"] if self.default is not None else []


@dataclass
class DjangoFloatField(DjangoModelField):
    default: T.Optional[float] = None
    field_name: str = "FloatField"

    def arg_default(self):
        return [f"default={self.default}"] if self.default is not None else []


@dataclass
class DjangoUuidField(DjangoModelField):
    field_name: str = "UUIDField"


@dataclass
class DjangoEmailField(DjangoModelField):
    default: T.Optional[str] = None
    field_name: str = "EmailField"

    def arg_default(self):
        return [f"default={self.default}"] if self.default else []


@dataclass
class DjangoDateField(DjangoModelField):
    field_name: str = "DateField"


@dataclass
class DjangoModel(Resource):
    name: str
    display_field_name: str = ""
    fields: T.List[DjangoModelField] = field(default_factory=list)

    @property
    def indexed_fields(self):
        return [x for x in self.fields if x.index]

    @property
    def slug_fields(self):
        return [x for x in self.fields if isinstance(x, DjangoSlugField)]

    @property
    def fk_fields(self):
        return [x for x in self.fields if isinstance(x, DjangoFkField)]

    @property
    def many_to_many_fields(self):
        return [x for x in self.fields if isinstance(x, DjangoManyToManyField)]


def import_type_spec(type_spec, django_model):
    django_model.name = type_spec.type_name
    django_model.display_field_name = type_spec.display_item_by

    for field_spec in type_spec.field_specs:
        args = dict(
            name=sn(field_spec.name),
            unique=field_spec.unique,
            required=field_spec.required,
            index=field_spec.index,
            help_text=field_spec.description,
        )

        if field_spec.field_type == "fk":
            if field_spec.through:
                raise Exception(
                    f"Fk fields cannot use 'through'. Use a relatedSet field instead. "
                    + f"For field: {field_spec.name} in type: {django_model.name}"
                )

            django_model.fields.append(
                DjangoFkField(
                    **args,
                    target=field_spec.target,
                    on_delete=_on_delete(field_spec),
                    admin_inline=field_spec.admin_inline,
                    related_name=(
                        f"{sn(l0(type_spec.type_name))}_set"
                        if field_spec.has_related_set
                        else "+"
                    ),
                )
            )
        elif field_spec.field_type == "relatedSet":
            if field_spec.through:
                django_model.fields.append(
                    DjangoManyToManyField(
                        **args,
                        target=field_spec.target,
                        through=field_spec.through,
                        admin_inline=field_spec.admin_inline,
                        related_name=(
                            "+"
                            if field_spec.through == "+"
                            else f"{sn(l0(type_spec.type_name))}_set"
                        ),
                    )
                )
        elif field_spec.field_type == "string":
            max_length = field_spec.field_type_attrs.get("maxLength")
            django_model.fields.append(
                DjangoCharField(
                    **args,
                    default=field_spec.default_value,
                    max_length=max_length,
                    choices=field_spec.field_type_attrs.get("choices"),
                )
                if max_length
                else DjangoTextField(
                    **args,
                    default=field_spec.default_value,
                )
            )
        elif field_spec.field_type == "slug":
            max_length = field_spec.field_type_attrs.get("maxLength")
            django_model.fields.append(
                DjangoSlugField(
                    **args,
                    **(dict(max_length=max_length) if max_length else {}),
                    slug_src=sn(field_spec.slug_src),
                )
            )
        elif field_spec.field_type == "json":
            django_model.fields.append(
                DjangoJsonField(
                    **args,
                    default=field_spec.default_value,
                )
            )
        elif field_spec.field_type == "url":
            max_length = field_spec.field_type_attrs.get("maxLength")
            django_model.fields.append(
                DjangoUrlField(
                    **args,
                    default=field_spec.default_value,
                    **(dict(max_length=max_length) if max_length else {}),
                )
            )
        elif field_spec.field_type == "boolean":
            django_model.fields.append(
                DjangoBooleanField(
                    **args,
                    default=field_spec.default_value,
                )
            )
        elif field_spec.field_type == "int":
            django_model.fields.append(
                DjangoIntegerField(
                    **args,
                    default=int(field_spec.default_value)
                    if field_spec.default_value is not None
                    else None,
                )
            )
        elif field_spec.field_type == "float":
            django_model.fields.append(
                DjangoFloatField(
                    **args,
                    default=float(field_spec.default_value)
                    if field_spec.default_value is not None
                    else None,
                )
            )
        elif field_spec.field_type == "uuid":
            django_model.fields.append(
                DjangoUuidField(
                    **args,
                )
            )
        elif field_spec.field_type == "email":
            django_model.fields.append(
                DjangoEmailField(
                    **args,
                    default=field_spec.default_value,
                )
            )
        elif field_spec.field_type == "date":
            django_model.fields.append(
                DjangoDateField(
                    **args,
                )
            )
        else:
            raise ValueError(f"Unknown field type: {field_spec.field_type}")

    django_model.fields = sorted(django_model.fields, key=lambda x: x.name)
