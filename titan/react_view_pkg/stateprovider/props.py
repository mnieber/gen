from moonleap import create_forward, str_to_term
from moonleap.blocks.verbs import provides


def state_provider_load(state_provider):
    forwards = []
    widget_spec = state_provider.widget_spec

    for state_term_str in widget_spec.get_value("states", default=[]):
        forwards += [
            create_forward(state_provider, provides, state_term_str),
        ]

    for pipeline_data in state_provider.widget_spec.get_value(
        "pipelines", default={}
    ).values():
        for term_str in pipeline_data:
            term = str_to_term(term_str)
            if term and term.tag in ("item", "item~list"):
                if term.is_title:
                    forwards.append(create_forward(state_provider, provides, term_str))

    return forwards
