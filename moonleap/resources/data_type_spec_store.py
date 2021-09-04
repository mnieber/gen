import os
import typing as T
from dataclasses import dataclass
from pathlib import Path

import yaml
from moonleap.session import get_session
from moonleap.utils.case import camel_to_snake, lower0, snake_to_camel, upper0
from moonleap.utils.inflect import plural


def _type(field_spec):
    t = field_spec.get("type")
    if t is not None:
        return t

    t = field_spec.get("$ref")
    prefix = "/data_types/"
    if t is not None and t.startswith(prefix):
        return FK(
            target=t[len(prefix) :],
            has_related_set=field_spec.get("has_related_set", True),
        )  # noqa: E203

    raise Exception(f"Unknown field type: {field_spec}")


def _default_value(field_spec):
    return field_spec.get("default", None)


def _unique(field_spec):
    return field_spec.get("unique", False)


def _description(field_spec):
    return field_spec.get("description")


def _load_data_type_dict(data_type_spec_dir, data_type_name):
    spec_fn = os.path.join(data_type_spec_dir, data_type_name + ".json")
    if not os.path.exists(spec_fn):
        raise Exception(f"File not found: {spec_fn}")

    with open(spec_fn) as f:
        data_type_dict = yaml.load(f, Loader=yaml.SafeLoader)
        if "properties" not in data_type_dict:
            raise Exception(f"Field 'properties' not found in {data_type_dict}")
        return data_type_dict


def _get_fields(data_type_dict):
    required = data_type_dict.get("required", [])
    private = data_type_dict.get("private", [])
    result = []
    for field_name, field_spec in data_type_dict["properties"].items():
        result.append(
            DataTypeField(
                default_value=_default_value(field_spec),
                description=_description(field_spec),
                field_type=_type(field_spec),
                name_snake=field_name,
                name=snake_to_camel(field_name),
                private=field_name in private,
                required=field_name in required,
                spec=field_spec,
                unique=_unique(field_spec),
            )
        )
    return result


@dataclass
class FK:
    target: str
    has_related_set: bool


@dataclass
class RelatedSet:
    target: str


@dataclass
class DataTypeField:
    field_type: T.Union[str, FK, RelatedSet]
    name_snake: str
    name: str
    private: bool
    required: bool
    spec: T.Any
    default_value: T.Any = None
    description: T.Optional[str] = None
    unique: bool = False


@dataclass
class DataTypeSpec:
    type_name: str
    fields: T.List[DataTypeField]


class DataTypeSpecStore:
    def __init__(self):
        self.spec_by_name = {}
        self.default_fields = [
            DataTypeField(
                name_snake="id",
                name="id",
                spec=dict(type="string"),
                required=True,
                private=False,
                field_type="string",
            ),
            DataTypeField(
                name_snake="name",
                name="name",
                spec=dict(type="string"),
                required=True,
                private=False,
                field_type="string",
            ),
        ]

    def _load_specs(self, data_types_dir):
        for spec_fn in Path(data_types_dir).glob("*.json"):
            data_type_name = spec_fn.stem
            data_type_dict = _load_data_type_dict(data_types_dir, data_type_name)

            spec = DataTypeSpec(
                type_name=data_type_name,
                fields=_get_fields(data_type_dict),
            )
            self.spec_by_name[data_type_name] = spec

        for data_type_name, spec in list(self.spec_by_name.items()):
            for field in spec.fields:
                if (
                    isinstance(field.field_type, FK)
                    and field.field_type.has_related_set
                ):
                    fk_spec = self.get_spec(field.field_type.target)
                    fk_spec.fields.append(
                        DataTypeField(
                            name=lower0(plural(spec.type_name)),
                            name_snake=lower0(camel_to_snake(plural(spec.type_name))),
                            spec=fk_spec,
                            required=False,
                            private=field.private,
                            field_type=RelatedSet(target=spec.type_name),
                        )
                    )

    def get_spec(self, data_type_name):
        if not self.spec_by_name:
            self._load_specs(
                os.path.join(get_session().settings["spec_dir"], "data_types")
            )

        data_type_name = upper0(data_type_name)
        if data_type_name not in self.spec_by_name:
            self.spec_by_name[data_type_name] = DataTypeSpec(
                type_name=data_type_name, fields=self.default_fields
            )

        return self.spec_by_name[data_type_name]


data_type_spec_store = DataTypeSpecStore()
