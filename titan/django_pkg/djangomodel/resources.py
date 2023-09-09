import typing as T
from dataclasses import dataclass, field

from moonleap import RenderMixin, Resource
from moonleap.utils.case import sn, snake_to_kebab
from titan.typespec.field_spec import FieldSpec
from titan.typespec.type_spec import TypeSpec

verbose_name_block_list = ["id", "sort_pos", "slug"]


@dataclass
class DjangoModelField(Resource):
    field_spec: FieldSpec
    name: str
    field_name: str
    help_text: T.Optional[str] = None
    translation_id: T.Optional[T.Union[str, bool]] = None

    def field_args(self, django_model):
        return []

    def arg_null_blank(self):
        return ["null=True", "blank=True"] if self.field_spec.is_optional else []

    def arg_unique(self):
        return ["unique=True"] if self.field_spec.unique else []

    def arg_help_text(self):
        return [f"help_text={self.help_text}"] if self.help_text else []

    def arg_primary_key(self):
        return ["primary_key=True"] if self.field_spec.primary_key else []

    def arg_readonly(self):
        return ["editable=False"] if self.field_spec.readonly else []

    def arg_verbose_name(self):
        return (
            [f'verbose_name=tr("{self.translation_id}")']
            if (self.translation_id and self.name not in verbose_name_block_list)
            else []
        )

    def arg_default(self):
        return (
            [f"default={self.field_spec.default_value}"]
            if self.field_spec.default_value is not None
            else []
        )

    def body(self, django_model):
        args = [x for x in self.field_args(django_model) if x is not None] + [
            *self.arg_primary_key(),
            *self.arg_default(),
            *self.arg_null_blank(),
            *self.arg_unique(),
            *self.arg_readonly(),
            *self.arg_help_text(),
            *self.arg_verbose_name(),
        ]
        args_str = ", ".join(args)
        return f"{self.field_name}({args_str})"


@dataclass
class DjangoFkField(DjangoModelField):
    field_name: str = "models.ForeignKey"

    def field_args(self, django_model):
        related_name = self.field_spec.related_name or "+"
        target = (
            f'"{self.field_spec.target}"'
            if django_model.type_spec.type_name == self.field_spec.target
            else self.field_spec.target
        )
        return [
            target,
            "on_delete=models.SET_NULL"
            if self.field_spec.set_null
            else "on_delete=models.CASCADE",
            *([f'related_name="{sn(related_name)}"'] if related_name else []),
        ]


@dataclass
class DjangoCharField(DjangoModelField):
    field_name: str = "models.CharField"

    def arg_default(self):
        return (
            [f'default="{self.field_spec.default_value}"']
            if self.field_spec.default_value
            else []
        )

    def field_args(self, django_model):
        choice_items = (
            [
                f'("{x[0]}", tr("{snake_to_kebab(x[1])}"))'
                for x in self.field_spec.choices or []
            ]
            if django_model.module.django_app.use_translation
            else [f'("{x[0]}", "{x[1]}")' for x in self.field_spec.choices or []]
        )
        choices_arg = f"choices=[{', '.join(choice_items)}]" if choice_items else None
        return [
            f"max_length={self.field_spec.max_length}",
            choices_arg,
        ]


@dataclass
class DjangoTextField(DjangoModelField):
    field_name: str = "models.TextField"

    def arg_default(self):
        return (
            [f'default="{self.field_spec.default_value}"']
            if self.field_spec.default_value
            else []
        )


@dataclass
class DjangoJsonField(DjangoModelField):
    field_name: str = "models.JSONField"

    def arg_default(self):
        return (
            [f"default={self.field_spec.default_value}"]
            if self.field_spec.default_value
            else []
        )


@dataclass
class DjangoSlugField(DjangoModelField):
    slug_src: T.Optional[str] = None
    field_name: str = "models.SlugField"

    def field_args(self, django_model):
        return [f"max_length={self.field_spec.max_length}"]


@dataclass
class DjangoImageField(DjangoModelField):
    field_name: str = "models.ImageField"

    def field_args(self, django_model):
        return [
            f'upload_to="img/{django_model.name}.{self.name}"',
            "validators=[validate_image_file]",
        ]


@dataclass
class DjangoMarkdownField(DjangoModelField):
    field_name: str = "MartorField"

    def field_args(self, django_model):
        return []


@dataclass
class DjangoUrlField(DjangoModelField):
    field_name: str = "models.URLField"

    def arg_default(self):
        return (
            [f'default="{self.field_spec.default_value}"']
            if self.field_spec.default_value
            else []
        )

    def field_args(self, django_model):
        return [f"max_length={self.field_spec.max_length}"]


@dataclass
class DjangoBooleanField(DjangoModelField):
    field_name: str = "models.BooleanField"

    def arg_default(self):
        return (
            [f'default={"True" if self.field_spec.default_value else "False"}']
            if self.field_spec.default_value in (True, False)
            else []
        )


@dataclass
class DjangoIntegerField(DjangoModelField):
    field_name: str = "models.IntegerField"

    def arg_default(self):
        return (
            [f"default={self.field_spec.default_value}"]
            if self.field_spec.default_value is not None
            else []
        )


@dataclass
class DjangoFloatField(DjangoModelField):
    field_name: str = "models.FloatField"

    def arg_default(self):
        return (
            [f"default={self.field_spec.default_value}"]
            if self.field_spec.default_value is not None
            else []
        )


@dataclass
class DjangoUuidField(DjangoModelField):
    field_name: str = "models.UUIDField"


@dataclass
class DjangoEmailField(DjangoModelField):
    field_name: str = "models.EmailField"

    def arg_default(self):
        return (
            [f"default={self.field_spec.default_value}"]
            if self.field_spec.default_value
            else []
        )


@dataclass
class DjangoDateField(DjangoModelField):
    field_name: str = "models.DateField"


@dataclass
class DjangoModel(RenderMixin, Resource):
    name: str
    kebab_name: str
    type_spec: T.Optional[TypeSpec] = None
    fields: T.List[DjangoModelField] = field(default_factory=list)

    @property
    def indexed_fields(self):
        return [x for x in self.fields if x.field_spec.is_indexed]

    @property
    def slug_fields(self):
        return [x for x in self.fields if isinstance(x, DjangoSlugField)]

    @property
    def fk_fields(self):
        return [x for x in self.fields if isinstance(x, DjangoFkField)]
