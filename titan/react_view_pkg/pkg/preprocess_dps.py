import re

import ramda as R

from moonleap.utils.fp import append_uniq

pattern = r"\bprops\.(?P<name>[a-zA-Z0-9_]+)\b"


def preprocess_dps(widget_spec):
    # Add dps to the __dps__ key in widget_spec.root
    dps = widget_spec.root.src_dict.setdefault("__dps__", [])
    props = widget_spec.root.src_dict.setdefault("__props__", [])
    for value in _get_values(widget_spec):
        if dps_name := get_dps_name(value):
            if dps_name not in props:
                append_uniq(dps, dps_name)

    # Process dps that appear in __pipelines__
    if pipeline_datas := widget_spec.src_dict.get("__pipelines__", {}):
        for pipeline_name, pipeline_data in pipeline_datas.items():
            if get_dps_name(R.head(pipeline_data)):
                pipeline_data.insert(0, "component:props")


def get_dps_name(value):
    if m := re.search(pattern, value):
        return m.group("name")
    return None


def _get_values(widget_spec):
    q = [dict(widget_spec.values)]

    while q:
        value = q.pop()
        if isinstance(value, dict):
            q.extend(value.values())
        elif isinstance(value, list):
            q.extend(value)
        else:
            if isinstance(value, str):
                yield value
