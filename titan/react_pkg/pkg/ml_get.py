def ml_react_app(x):
    from titan.react_pkg.component import Component
    from titan.react_pkg.module import Module

    if isinstance(x, Component):
        return x.module.react_app
    if isinstance(x, Module):
        return x.react_app
    raise Exception(f"ml_react_app: unknown {x}")


def ml_graphql_api(x):
    from titan.react_pkg.reactapp import ReactApp

    if isinstance(x, ReactApp):
        return x.api_module.graphql_api
    raise Exception(f"ml_graphql_api: unknown {x}")
