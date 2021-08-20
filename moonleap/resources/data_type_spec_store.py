import os
import typing as T
from dataclasses import dataclass

import yaml
from moonleap.session import get_session
from moonleap.utils.case import snake_to_camel, upper0


def _type(field_spec):
    t = field_spec.get("type")
    if t is not None:
        return t

    t = field_spec.get("$ref")
    prefix = "/data_types/"
    if t is not None and t.startswith(prefix):
        return FK(t[len(prefix) :])  # noqa: E203

    raise Exception(f"Unknown field type: {field_spec}")


def _load_data_type_dict(data_type_spec_dir, data_type_name):
    spec_fn = os.path.join(data_type_spec_dir, "data_types", data_type_name + ".json")
    if not os.path.exists(spec_fn):
        return None

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
                name_snake=field_name,
                name=snake_to_camel(field_name),
                spec=field_spec,
                required=field_name in required,
                private=field_name in private,
                field_type=_type(field_spec),
            )
        )
    return result


@dataclass
class FK:
    target: str


@dataclass
class DataTypeField:
    name_snake: str
    name: str
    spec: T.Any
    required: bool
    private: bool
    field_type: T.Union[str, FK]
    default_value: str = ""


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

    def get_spec(self, data_type_name):
        data_type_name = upper0(data_type_name)
        if data_type_name not in self.spec_by_name:
            data_type_dict = _load_data_type_dict(
                get_session().settings["spec_dir"], data_type_name
            )

            spec = DataTypeSpec(
                type_name=data_type_name,
                fields=_get_fields(data_type_dict)
                if data_type_dict
                else self.default_fields,
            )
            self.spec_by_name[data_type_name] = spec

        return self.spec_by_name[data_type_name]


data_type_spec_store = DataTypeSpecStore()
