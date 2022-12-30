import typing as T
from dataclasses import dataclass, field

from moonleap import RenderMixin, Resource
from moonleap.blocks.parser.utils.get_meta import get_meta
from moonleap.utils.case import l0
from titan.types_pkg.typeregistry import get_type_reg
from typespec.api_spec import ApiSpec


@dataclass
class Query(RenderMixin, Resource):
    name: str
    api_spec: "ApiSpec" = field(repr=False)


@dataclass
class Mutation(RenderMixin, Resource):
    name: str
    api_spec: "ApiSpec" = field(repr=False)
    items_saved: T.List[str] = field(default_factory=list)
    item_lists_saved: T.List[str] = field(default_factory=list)
    items_deleted: T.List[str] = field(default_factory=list)
    item_lists_deleted: T.List[str] = field(default_factory=list)


@dataclass
class ApiRegistry(Resource):
    def __post_init__(self):
        self._api_spec_by_name = {}
        self._query_by_query_name = {}
        self._mutation_by_mutation_name = {}

    def setdefault(self, name, default_value):
        if not self.has(name):
            self._api_spec_by_name[name] = default_value

    def has(self, name):
        return bool(self._api_spec_by_name.get(name, None))

    def get(self, name, default="__not_set__") -> ApiSpec:
        result = self._api_spec_by_name.get(name, None)
        if result is None:
            if default == "__not_set__":
                raise Exception(f"Missing api spec: {name}")
            return T.cast(ApiSpec, default)
        return result

    def api_specs(self):
        return self._api_spec_by_name.values()

    def get_query(self, query_name):
        if query_name not in self._query_by_query_name:
            api_spec = self.get(query_name)
            if not api_spec.is_mutation:
                query = Query(name=query_name, api_spec=api_spec)
                query.meta = get_meta(f"{query_name}:query")
            else:
                query = None
            self._query_by_query_name[query_name] = query
        return self._query_by_query_name[query_name]

    def get_mutation(self, mutation_name):
        if mutation_name not in self._mutation_by_mutation_name:
            api_spec = self.get(mutation_name)
            if api_spec.is_mutation:
                mutation = Mutation(name=mutation_name, api_spec=api_spec)
                mutation.meta = get_meta(f"{mutation_name}:mutation")

                for type_name_saved, is_list in api_spec.saves:
                    data = _data(type_name_saved, is_list)
                    if is_list:
                        mutation.item_lists_saved.append(data)
                    else:
                        mutation.items_saved.append(data)

                for type_name_saved, is_list in api_spec.deletes:
                    data = _data(type_name_saved, is_list)
                    if is_list:
                        mutation.item_lists_deleted.append(data)
                    else:
                        mutation.items_deleted.append(data)
            else:
                mutation = None
            self._mutation_by_mutation_name[mutation_name] = mutation
        return self._mutation_by_mutation_name[mutation_name]

    @property
    def queries(self):
        return [
            self.get_query(api_spec.name)
            for api_spec in self.api_specs()
            if not api_spec.is_mutation
        ]

    @property
    def mutations(self):
        return [
            self.get_mutation(api_spec.name)
            for api_spec in self.api_specs()
            if api_spec.is_mutation
        ]


def _data(type_name, is_list):
    item_name = l0(type_name)
    return (
        get_type_reg().get_item_list(item_name)
        if is_list
        else get_type_reg().get_item(item_name)
    )
