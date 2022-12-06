from moonleap import create_forward
from moonleap.verbs import provides


def state_provider_load(state_provider):
    forwards = []
    widget_spec = state_provider.widget_spec

    for state_term in widget_spec.src_dict.get("__states__", []):
        forwards.append(create_forward(state_provider, provides, state_term))

    for pipeline in state_provider.pipelines:
        for res in pipeline.resources:
            if res.meta.term.tag in ("item", "item~list"):
                if res.meta.term.is_title:
                    forwards.append(create_forward(state_provider, provides, res))

    return forwards
