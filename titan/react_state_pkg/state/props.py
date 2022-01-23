import bisect
import os

import ramda as R
from moonleap import u0
from moonleap.utils.inflect import plural
from titan.api_pkg.pkg.ml_name import (
    ml_form_type_spec_from_item_name,
    ml_type_spec_from_item_name,
)
from titan.react_pkg.pkg.field_spec_to_ts_type import field_spec_to_ts_type
from titan.react_pkg.pkg.ml_get import ml_react_app
from titan.react_pkg.pkg.ts_var import ts_form_type, ts_type


def _find_module_that_provides_item_list(react_app, item_name):
    for module in react_app.modules:
        for state in module.states:
            for item_list in state.item_lists_provided:
                if item_list.item_name == item_name:
                    return module
    return None


def bvrs_by_item_name(self):
    result = dict()
    for bvr in self.behaviors:
        bvrs = result.setdefault(bvr.item_name, [])
        pos = bisect.bisect_left(R.map(R.prop("name"))(bvrs), bvr.name)
        result[bvr.item_name].insert(pos, bvr)
    for item_list in self.item_lists_provided:
        result.setdefault(item_list.item_name, [])
    return result


def type_import_path(self, item_name):
    module = _find_module_that_provides_item_list(ml_react_app(self), item_name)
    if module:
        return f"{module.module_path}/types"
    return None


def get_context(state):
    _ = lambda: None

    class Sections:
        def constructor(self):
            indent = "  "
            result = []

            for item_name, bvrs in state.bvrs_by_item_name.items():
                result += [f"{plural(item_name)} = {{"]
                for bvr in bvrs:
                    result += [bvr.sections.constructor()]
                result += [r"};"]

            return os.linesep.join([(indent + x) for x in result])

        def callbacks(self):
            indent = "  "
            result = []

            for item_name, bvrs in state.bvrs_by_item_name.items():
                redRoses = plural(item_name)

                body = []
                for bvr in bvrs:
                    body += [bvr.sections.callbacks(state.behaviors)]

                result += [f"_set{u0(redRoses)}Callbacks(props: PropsT) {{"]

                if body:
                    result += [f"  const ctr = this.{redRoses};"]
                    result += body

                result += [r"}", ""]

            return os.linesep.join([(indent + x) for x in result])

        def declare_policies(self, item_name):
            indent = "    "
            items = plural(item_name)
            result = [
                f"const Inputs_items = [Inputs, '{items}', this] as CMT;",
                f"const Outputs_display = [Outputs, '{items}Display', this] as CMT;",  # noqa: E501
            ]

            return os.linesep.join([(indent + x) for x in result])

        def policies(self):
            facet_names = [x.name for x in state.behaviors]
            indent = "      "
            result = []

            if "filtering" not in facet_names:
                result += [
                    r"Skandha.mapDataToFacet(Outputs_display, getm(Inputs_items)),",
                ]

            return os.linesep.join([(indent + x) for x in result])

        def define_type(self, item):
            result = []
            type_spec = ml_type_spec_from_item_name(item.item_name)

            result.append(f"export type {ts_type(item)} = {{")
            for field_spec in type_spec.field_specs:
                if field_spec.private:
                    continue

                t = field_spec_to_ts_type(field_spec, fk_as_str=True)
                postfix = "Id" if field_spec.field_type == "fk" else ""
                result.append(f"  {field_spec.name}{postfix}: {t};")
            result.append(f"}}")

            return "\n".join(result)

        def define_form_type(self, item):
            if not item.item_type.form_type:
                return ""

            type_spec = ml_form_type_spec_from_item_name(item.item_name)

            result = []
            result.append(f"export type {ts_form_type(item)} = {{")

            for field_spec in type_spec.field_specs:
                if field_spec.private:
                    continue

                t = field_spec_to_ts_type(field_spec, fk_as_str=True)
                result.append(f"  {field_spec.name}: {t};")

            result.append(r"}")

            return "\n".join(result)

    return dict(sections=Sections(), _=_)
