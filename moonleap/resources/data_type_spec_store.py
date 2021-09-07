import os
import typing as T
from dataclasses import dataclass, field
from pathlib import Path

import ramda as R
import yaml
from moonleap.session import get_session
from moonleap.utils.case import camel_to_snake, lower0, snake_to_camel, upper0
from moonleap.utils.inflect import plural

fk_prefix = "/data_types/"


def _type_and_attrs(field_spec):
    attrs = {}
    t = field_spec.get("type")

    if t is None:
        ref = field_spec.get("$ref", "")
        if ref.startswith(fk_prefix):
            t = "fk"
            attrs["target"] = ref[len(fk_prefix) :]  # noqa: E203
            attrs["has_related_set"] = (field_spec.get("has_related_set", True),)
    else:
        if "onDelete" in field_spec:
            attrs["on_delete"] = field_spec["onDelete"]

        if "maxLength" in field_spec:
            attrs["max_length"] = field_spec["maxLength"]

    if t is None:
        raise Exception(f"Unknown field type: {field_spec}")

    return t, attrs


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
        t, attrs = _type_and_attrs(field_spec)

        result.append(
            DataTypeField(
                default_value=_default_value(field_spec),
                description=_description(field_spec),
                field_type=t,
                field_type_attrs=attrs,
                name_snake=field_name,
                name=snake_to_camel(field_name),
                private=field_name in private,
                required=field_name in required,
                unique=_unique(field_spec),
            )
        )
    return result


@dataclass
class DataTypeField:
    field_type: str
    name_snake: str
    name: str
    private: bool
    required: bool
    default_value: T.Any = None
    description: T.Optional[str] = None
    unique: bool = False
    field_type_attrs: dict = field(default_factory=dict)


@dataclass
class DataTypeSpec:
    type_name: str
    field_by_name: T.Dict[str, DataTypeField]
    query_item_by: T.List[str] = field(default_factory=list)
    query_item_list_by: T.List[str] = field(default_factory=list)


class DataTypeSpecStore:
    def __init__(self):
        self.spec_by_name = {}
        self.default_field_by_name = R.index_by(
            R.prop("name"),
            [
                DataTypeField(
                    name_snake="id",
                    name="id",
                    required=True,
                    private=False,
                    field_type="string",
                ),
                DataTypeField(
                    name_snake="name",
                    name="name",
                    required=True,
                    private=False,
                    field_type="string",
                ),
            ],
        )

    def _load_specs(self, data_types_dir):
        for spec_fn in Path(data_types_dir).glob("*.json"):
            data_type_name = spec_fn.stem
            data_type_dict = _load_data_type_dict(data_types_dir, data_type_name)

            spec = DataTypeSpec(
                type_name=data_type_name,
                field_by_name=R.index_by(R.prop("name"), _get_fields(data_type_dict)),
                query_item_by=data_type_dict.get("query_item_by", ["id"]),
                query_item_list_by=data_type_dict.get("query_item_list_by", []),
            )
            self.spec_by_name[data_type_name] = spec

        for data_type_name, spec in list(self.spec_by_name.items()):
            for _, field in spec.field_by_name.items():
                if field.field_type == "fk" and field.field_type_attrs.get(
                    "has_related_set"
                ):
                    fk_spec = self.get_spec(field.field_type_attrs["target"])
                    name = lower0(plural(spec.type_name))
                    fk_spec.field_by_name[name] = DataTypeField(
                        name=name,
                        name_snake=camel_to_snake(name),
                        required=False,
                        private=field.private,
                        field_type="related_set",
                        field_type_attrs=dict(target=spec.type_name),
                    )

    def get_spec(self, data_type_name):
        if not self.spec_by_name:
            self._load_specs(
                os.path.join(get_session().settings["spec_dir"], "data_types")
            )

        data_type_name = upper0(data_type_name)
        if data_type_name not in self.spec_by_name:
            self.spec_by_name[data_type_name] = DataTypeSpec(
                type_name=data_type_name, field_by_name=self.default_field_by_name
            )

        return self.spec_by_name[data_type_name]


data_type_spec_store = DataTypeSpecStore()
