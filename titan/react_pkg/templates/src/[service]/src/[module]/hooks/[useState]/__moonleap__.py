from moonleap import u0


def get_helpers(_):
    class Helpers:
        state = _.state_provider.state

        def __init__(self):
            pass

    return Helpers()


def get_meta_data_by_fn(_, __):
    return {
        "useState.ts.j2": {
            "name": f"use{u0(_.state.name)}.ts",
        },
        "useState.index.ts.j2": {
            "name": f"index.ts",
        },
    }


def get_contexts(_):
    return [
        dict(state=state, state_provider=state.state_provider)
        for state in _.module.states
    ]
