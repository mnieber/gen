import ramda as R
from moonleap import get_root_resource
from moonleap.utils.case import camel_to_kebab, sn
from titan.django_pkg.djangomodel.resources import (
    DjangoBooleanField,
    DjangoCharField,
    DjangoDateField,
    DjangoEmailField,
    DjangoFkField,
    DjangoFloatField,
    DjangoImageField,
    DjangoIntegerField,
    DjangoJsonField,
    DjangoMarkdownField,
    DjangoSlugField,
    DjangoTextField,
    DjangoUrlField,
    DjangoUuidField,
)


def import_type_spec(type_spec, django_model):
    django_model.type_spec = type_spec
    django_model.name = type_spec.type_name

    field_specs = [x for x in type_spec.get_field_specs() if x.has_model]
    django_app = django_model.module.django_app
    for field_spec in field_specs:
        kebab_name = camel_to_kebab(field_spec.name)
        args = dict(
            field_spec=field_spec,
            help_text=(
                None
                if not field_spec.help
                else f'tr("{type_spec.type_name}.{field_spec.name}.help_text")'
                if django_app.use_translation
                else '"Moonleap Todo"'
            ),
            name=sn(field_spec.name),
            translation_id=(kebab_name if django_app.use_translation else None),
        )

        if field_spec.field_type == "fk":
            django_model.fields.append(DjangoFkField(**args))
        elif field_spec.field_type == "relatedSet":
            pass
        elif field_spec.field_type == "slug":
            slug_sources = [x.name for x in field_specs if x.is_slug_src]
            django_model.fields.append(
                DjangoSlugField(
                    **args,
                    slug_src=sn(slug_sources[0]) if slug_sources else None,
                )
            )
        elif field_spec.field_type == "string":
            django_model.fields.append(DjangoCharField(**args))
        elif field_spec.field_type == "text":
            django_model.fields.append(DjangoTextField(**args))
        elif field_spec.field_type in ("json"):
            django_model.fields.append(DjangoJsonField(**args))
        elif field_spec.field_type in ("tags"):
            django_model.fields.append(DjangoJsonField(**args))
        elif field_spec.field_type == "url":
            django_model.fields.append(DjangoUrlField(**args))
        elif field_spec.field_type == "boolean":
            django_model.fields.append(DjangoBooleanField(**args))
        elif field_spec.field_type == "int":
            django_model.fields.append(DjangoIntegerField(**args))
        elif field_spec.field_type == "float":
            django_model.fields.append(DjangoFloatField(**args))
        elif field_spec.field_type == "uuid":
            django_model.fields.append(DjangoUuidField(**args))
        elif field_spec.field_type == "email":
            django_model.fields.append(DjangoEmailField(**args))
        elif field_spec.field_type == "date":
            django_model.fields.append(DjangoDateField(**args))
        elif field_spec.field_type == "image":
            django_model.fields.append(DjangoImageField(**args))
        elif field_spec.field_type == "markdown":
            get_root_resource().set_flags(["django/hasMarkdownFields"])
            django_model.fields.append(DjangoMarkdownField(**args))
        else:
            raise ValueError(f"Unknown field type: {field_spec.field_type}")

    django_model.fields = sorted(django_model.fields, key=lambda x: x.name)
