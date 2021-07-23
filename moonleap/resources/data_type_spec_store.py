import os
import typing as T
from dataclasses import dataclass

import yaml
from moonleap import kebab_to_camel
from moonleap.session import get_session
from moonleap.utils.case import kebab_to_camel, snake_to_camel, upper0


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
    result = []
    for field_name, field_spec in data_type_dict["properties"].items():
        result.append(
            DataTypeField(
                name_snake=field_name,
                name_camel=snake_to_camel(field_name),
                type=field_spec.get("type", "string"),
            )
        )
    return result


@dataclass
class DataTypeField:
    name_snake: str
    name_camel: str
    type: str


@dataclass
class DataTypeSpec:
    type_name: str
    fields: T.List[DataTypeField]


class DataTypeSpecStore:
    def __init__(self):
        self.spec_by_name = {}
        self.default_fields = [
            DataTypeField(name_snake="id", name_camel="id", type="string"),
            DataTypeField(name_snake="name", name_camel="name", type="string"),
        ]

    def get_spec(self, data_type_name):
        data_type_name = upper0(kebab_to_camel(data_type_name))
        if data_type_name not in self.spec_by_name:
            data_type_dict = _load_data_type_dict(
                get_session().settings["spec_dir"], data_type_name
            )
            spec = DataTypeSpec(
                data_type_name,
                _get_fields(data_type_dict) if data_type_dict else self.default_fields,
            )
            self.spec_by_name[data_type_name] = spec

        return self.spec_by_name[data_type_name]


data_type_spec_store = DataTypeSpecStore()
