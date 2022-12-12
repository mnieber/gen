import typing as T
from collections import defaultdict
from dataclasses import dataclass, field

from moonleap import Resource, u0
from moonleap.parser.get_global_block import get_global_block
from moonleap.parser.term import word_to_term
from moonleap.resource import ResourceMetaData
from moonleap.utils.case import l0
from titan.types_pkg.pkg.default_field_specs_store import DefaultFieldSpecsStore
from titan.types_pkg.pkg.type_spec import TypeSpec

_default_type_spec_placeholder = TypeSpec(type_name="placeholder", field_specs=[])


@dataclass
class Item(Resource):
    item_name: str
    item_list: "ItemList" = field(repr=False)
    type_spec: TypeSpec = field(repr=False)


@dataclass
class ItemList(Resource):
    item_name: str
    item: Item = field(repr=False)
    type_spec: "TypeSpec" = field(repr=False)


@dataclass
class TypeRegistry(Resource):
    def __post_init__(self):
        self._type_spec_by_type_name: T.Dict[str, "TypeSpec"] = {}
        self.default_field_specs_store = DefaultFieldSpecsStore()
        self.parents_by_type_name = defaultdict(list)
        self._item_by_item_name = dict()
        self._item_list_by_item_name = dict()

    def setdefault(self, type_name, default_value):
        assert type_name and type_name[0] == type_name[0].upper()

        if not self.has(type_name):
            self._type_spec_by_type_name[type_name] = default_value

    def has(self, type_name):
        assert type_name and type_name[0] == type_name[0].upper()

        return type_name in self._type_spec_by_type_name

    def get(self, type_name, default=_default_type_spec_placeholder) -> TypeSpec:
        assert type_name and type_name[0] == type_name[0].upper()

        type_spec = self._type_spec_by_type_name.get(type_name, None)
        if type_spec is not None:
            return type_spec

        return (
            TypeSpec(
                type_name=type_name,
                field_specs=self.default_field_specs_store.get_field_specs(type_name),
            )
            if default is _default_type_spec_placeholder
            else default
        )

    def get_item(self, item_name):
        if item_name not in self._item_by_item_name:
            self._create_item_and_item_list(item_name)
        return self._item_by_item_name[item_name]

    def get_item_list(self, item_name):
        if item_name not in self._item_list_by_item_name:
            self._create_item_and_item_list(item_name)
        return self._item_list_by_item_name[item_name]

    def _create_item_and_item_list(self, item_name):
        type_spec = self.get(u0(item_name), default=None)
        if not type_spec:
            raise Exception(f"Cannot create item. Unknown type-spec {u0(item_name)}")
        item = Item(item_name=item_name, type_spec=type_spec, item_list=None)  # type: ignore
        item.meta = _get_meta(f"{item_name}:item")
        item_list = ItemList(item_name=item_name, type_spec=type_spec, item=item)
        item_list.meta = _get_meta(f"{item_name}:item~list")
        item.item_list = item_list
        self._item_list_by_item_name[item_name] = item_list
        self._item_by_item_name[item_name] = item

    def type_specs(self) -> T.List[TypeSpec]:
        return list(self._type_spec_by_type_name.values())

    @property
    def items(self) -> T.List[Item]:
        return [
            self.get_item(l0(type_spec.type_name))
            for type_spec in self.type_specs()
            if not type_spec.is_form
        ]

    def register_parent_child(self, parent_type_name, child_type_name):
        self.parents_by_type_name[child_type_name].append(parent_type_name)


def _get_meta(word):
    return ResourceMetaData(
        term=word_to_term(word),
        block=get_global_block(),
        base_tags=[],
    )
