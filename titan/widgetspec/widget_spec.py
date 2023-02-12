import typing as T
from dataclasses import dataclass, field
from pprint import pprint as pp

import ramda as R

from moonleap import append_uniq
from moonleap.blocks.term import match_term_to_pattern
from moonleap.utils.get_id import get_id
from titan.widgetspec.create_widget_class_name import create_widget_class_name
from titan.widgetspec.div import Div
from titan.widgetspec.widget_spec_memo import WidgetSpecMemoContext


@dataclass
class WidgetSpec:
    widget_base_types: T.List[str] = field(default_factory=list)
    # The sub-widget specs inside this widget spec
    child_widget_specs: T.List["WidgetSpec"] = field(repr=False, default_factory=list)
    # The widget specs that wrap this widget spec
    wrapper_widget_specs: T.List["WidgetSpec"] = field(repr=False, default_factory=list)
    div: Div = field(default_factory=Div)
    widget_name: T.Optional[str] = None
    module_name: T.Optional[str] = None
    place: T.Optional[str] = None
    values: T.Dict[str, str] = field(default_factory=dict)
    id: str = field(default_factory=get_id)
    parent: T.Optional["WidgetSpec"] = field(repr=False, default=None)
    # This is the dict from which the widget_spec was created
    src_dict: T.Dict[str, str] = field(default_factory=dict)
    # Tags are used to collect any kind of information use it in the root builder
    tags: list = field(default_factory=list)

    # The following fields are None by default because they should only
    # exist after the call to 'hydrate'
    pipelines: list = field(default_factory=list)
    named_props: list = field(default_factory=list)
    named_default_props: list = field(default_factory=list)

    # Private
    _widget_class_name: str = ""

    def add_child_widget_spec(self, widget_spec):
        if [x for x in self.child_widget_specs if x.id == widget_spec.id]:
            raise Exception(f"Duplicate widget_spec {widget_spec.id}")
        self.child_widget_specs.append(widget_spec)

    def add_wrapper_widget_spec(self, widget_spec):
        if [x for x in self.wrapper_widget_specs if x.id == widget_spec.id]:
            raise Exception(f"Duplicate widget_spec {widget_spec.id}")
        self.wrapper_widget_specs.append(widget_spec)

    def remove_child_widget_spec(self, widget_spec):
        self.child_widget_specs = [
            x for x in self.child_widget_specs if x.id != widget_spec.id
        ]

    @property
    def is_component(self):
        return self.widget_name and ":" in self.widget_name

    @property
    def is_component_def(self):
        return bool(
            self.is_component
            and self.widget_base_types
            and self.widget_name not in self.widget_base_types
        )

    @property
    def widget_class_name(self):
        if not self._widget_class_name:
            self._widget_class_name = create_widget_class_name(self)
        return self._widget_class_name

    def set_widget_class_name(self, value):
        self._widget_class_name = value

    def get_place(self, place):
        return R.head(x for x in self.child_widget_specs if x.place == place)

    def memo(self, fields):
        return WidgetSpecMemoContext(self, fields)

    def get_value_by_name(self, name, default=None, recurse=False):
        ws = self
        while ws:
            value = ws.values.get(name)
            if value:
                return value
            ws = ws.parent if recurse else None
        return default

    @property
    def root(self):
        ws = self
        while ws.parent and not ws.is_component_def:
            ws = ws.parent
        return ws

    def get_pipeline_data(self, name, recurse=False):
        ws = self
        while ws:
            for pipeline_name, pipeline_data in ws.src_dict.get(
                "__pipelines__", {}
            ).items():
                if pipeline_name == name:
                    return pipeline_data
            ws = ws.parent if recurse else None
        return None

    def get_pipeline_by_name(self, name, recurse=False):
        ws = self
        while ws:
            for pipeline in ws.pipelines:
                if pipeline.name == name:
                    return pipeline
            ws = ws.parent if recurse else None
        return None

    def get_data_path(self, obj, recurse=False):
        ws = self
        data_path = None
        while ws:
            pipeline, data_path = ws._get_pipeline(obj)
            if not data_path:
                for named_res_set in (ws.named_props, ws.named_default_props):
                    for named_prop in named_res_set:
                        t = obj.meta.term
                        if match_term_to_pattern(named_prop.meta.term, t):
                            return f"props.{named_prop.typ.ts_var}"
            ws = ws.parent if recurse else None
        return data_path

    @property
    def queries(self):
        result = []

        for pipeline in self.pipelines:
            pipeline_source = pipeline.source
            if pipeline_source.meta.term.tag == "query":
                append_uniq(result, pipeline_source)

        return result

    @property
    def mutations(self):
        result = []

        for pipeline in self.pipelines:
            pipeline_source = pipeline.source
            if pipeline_source.meta.term.tag == "mutation":
                append_uniq(result, pipeline_source)

        return result

    def _get_pipeline(self, obj):
        try:
            results = []
            for pipeline in self.pipelines:
                if data_path := pipeline.data_path(obj):
                    results.append((pipeline, data_path))

            if len(results) > 1:
                raise Exception(
                    "More than one data path found for " + f"{obj}: {results}"
                )
            return results[0] if results else (None, None)
        except Exception as e:
            print(f"\nIn widget_spec {self}")
            raise

    @property
    def debug(self):
        pp(self.src_dict)

    def add_tag(self, tag):
        append_uniq(self.tags, tag)

    def has_tag(self, tag):
        return tag in self.tags
