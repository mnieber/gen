import typing as T
from dataclasses import dataclass, field

from moonleap import Resource
from moonleap.utils.case import sn

from .utils import _on_delete


@dataclass
class DjangoModelField(Resource):
    name: str
    field_name: str
    required: T.Optional[bool] = field(init=False)
    unique: T.Optional[bool] = field(init=False)
    help_text: T.Optional[str] = field(init=False)

    def field_args(self):
        return []

    def arg_null_blank(self):
        return [] if self.required else ["null=True", "blank=True"]

    def arg_unique(self):
        return ["unique=True"] if self.unique else []

    def arg_help_text(self):
        return [f"help_text='{self.help_text}'"] if self.help_text else []

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
        return f"models.{self.field_name}({args_str})"


@dataclass
class DjangoFkField(DjangoModelField):
    target: str
    admin_inline: bool
    related_name: str
    on_delete: str
    field_name: str = "ForeignKeyField"

    def null_blank(self):
        return [] if self.required else ["blank=True"]

    def field_args(self):
        return [
            self.target,
            f"on_delete={self.on_delete}",
            f"related_name={self.related_name}",
        ]


@dataclass
class DjangoManyToManyField(DjangoModelField):
    target: str
    admin_inline: bool
    through: str
    related_name: str
    field_name: str = "ManyToManyField"

    def field_args(self):
        return [
            self.target,
            None if self.through == "+" else f"through={self.through}",
            f"related_name={self.related_name}",
        ]


@dataclass
class DjangoCharField(DjangoModelField):
    max_length: int
    default: str
    choices: T.List[str] = field(default_factory=list)
    field_name: str = "CharField"

    def arg_default(self):
        return [f'default="{field.default}"'] if field.default else []

    def field_args(self):
        choice_items = [f'("{x}", "{x}")' for x in self.choices]
        choices_arg = f"choices=[{', '.join(choice_items)}]" if choice_items else None
        return [f"max_length={self.max_length}", choices_arg]


@dataclass
class DjangoTextField(DjangoModelField):
    default: str
    field_name: str = "TextField"

    def arg_default(self):
        return [f'default="{field.default}"'] if field.default else []


@dataclass
class DjangoJsonField(DjangoModelField):
    default: str
    field_name: str = "JSONField"

    def arg_default(self):
        return [f'default="{field.default}"'] if field.default else []


@dataclass
class DjangoSlugField(DjangoModelField):
    max_length: int
    slug_src: str
    field_name: str = "SlugField"

    def field_args(self):
        return [
            f"max_length={self.max_length}",
        ]


@dataclass
class DjangoUrlField(DjangoModelField):
    max_length: int
    default: str
    field_name: str = "URLField"

    def arg_default(self):
        return [f'default="{field.default}"'] if field.default else []

    def field_args(self):
        return [
            f"max_length={self.max_length}",
        ]


@dataclass
class DjangoBooleanField(DjangoModelField):
    default: bool
    field_name: str = "BooleanField"

    def arg_default(self):
        return (
            [f'default={"True" if field.default_value else "False"}']
            if field.default_value in (True, False)
            else []
        )


@dataclass
class DjangoIntegerField(DjangoModelField):
    default: int
    field_name: str = "IntegerField"

    def arg_default(self):
        return (
            [f"default={field.default_value}"]
            if field.default_value is not None
            else []
        )


@dataclass
class DjangoFloatField(DjangoModelField):
    default: float
    field_name: str = "FloatField"

    def arg_default(self):
        return (
            [f"default={field.default_value}"]
            if field.default_value is not None
            else []
        )


@dataclass
class DjangoUuidField(DjangoModelField):
    field_name: str = "UUIDField"


@dataclass
class DjangoEmailField(DjangoModelField):
    default: str
    field_name: str = "EmailField"

    def arg_default(self):
        return [f"default={field.default_value}"] if field.default_value else []


@dataclass
class DjangoDateField(DjangoModelField):
    field_name: str = "DateField"


@dataclass
class DjangoModel(Resource):
    name: str
    fields: T.List[DjangoModelField] = field(default_factory=list)


def import_type_spec(type_spec, django_model):
    for field_spec in type_spec.get_field_specs():
        if field_spec.field_type == "fk":
            if field_spec.through:
                raise Exception(
                    f"Fk fields cannot use 'through'. Use a relatedSet field instead. "
                    + f"For field: {field.name} in type: {django_model.name}"
                )

            django_model.fields.append(
                DjangoFkField(
                    name=sn(field_spec.name),
                    target=field_spec.target,
                    on_delete=_on_delete(field_spec),
                    admin_inline=field_spec.admin_inline,
                    related_name=(
                        f"{sn(field_spec.target)}_set"
                        if field_spec.has_related_set
                        else "+"
                    ),
                )
            )
        elif field_spec.field_type == "relatedSet":
            if field_spec.through:
                django_model.fields.append(
                    DjangoManyToManyField(
                        name=sn(field_spec.name),
                        target=field_spec.target,
                        through=field_spec.through,
                        admin_inline=field_spec.admin_inline,
                        related_name=(
                            "+"
                            if field_spec.through == "+"
                            else f"{sn(field_spec.target)}_set"
                        ),
                    )
                )
        elif field_spec.field_type == "string":
            max_length = field_spec.field_type_attrs.get("maxLength")
            django_model.fields.append(
                DjangoCharField(
                    name=field_spec.name,
                    default=field_spec.default_value,
                    max_length=max_length,
                    choices=field.field_type_attrs.get("choices"),
                )
                if max_length
                else DjangoTextField(
                    name=field_spec.name,
                    default=field_spec.default_value,
                )
            )
        elif field_spec.field_type == "slug":
            django_model.fields.append(
                DjangoSlugField(
                    name=field_spec.name,
                    max_length=field_spec.field_type_attrs.get("maxLength"),
                    slug_src=sn(field_spec.slug_src),
                )
            )
        elif field_spec.field_type == "json":
            django_model.fields.append(
                DjangoJsonField(
                    name=field_spec.name,
                    default=field_spec.default_value,
                )
            )
        elif field_spec.field_type == "url":
            django_model.fields.append(
                DjangoUrlField(
                    name=field_spec.name,
                    default=field_spec.default_value,
                    max_length=field_spec.field_type_attrs.get("maxLength"),
                )
            )
        elif field_spec.field_type == "boolean":
            django_model.fields.append(
                DjangoBooleanField(
                    name=field_spec.name,
                    default=field_spec.default_value,
                )
            )
        elif field_spec.field_type == "int":
            django_model.fields.append(
                DjangoIntegerField(
                    name=field_spec.name,
                    default=int(field_spec.default_value),
                )
            )
        elif field_spec.field_type == "float":
            django_model.fields.append(
                DjangoFloatField(
                    name=field_spec.name,
                    default=float(field_spec.default_value),
                )
            )
        elif field_spec.field_type == "uuid":
            django_model.fields.append(DjangoUuidField(name=field_spec.name))
        elif field_spec.field_type == "email":
            django_model.fields.append(
                DjangoEmailField(
                    name=field_spec.name,
                    default=field_spec.default_value,
                )
            )
        elif field_spec.field_type == "date":
            django_model.fields.append(DjangoDateField(name=field_spec.name))
        else:
            raise ValueError(f"Unknown field type: {field_spec.field_type}")
