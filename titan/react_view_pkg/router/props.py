import os
import typing as T
from dataclasses import dataclass, field

import ramda as R
from moonleap.utils.join import join
from moonleap.utils.queue import Queue
from titan.react_pkg.pkg.ml_get import ml_react_app

from .create_route_name import create_route_name


@dataclass
class Elm:
    parent: T.Optional["Elm"] = None
    children: T.List["Elm"] = field(default_factory=list)
    dep_chains: T.List[T.Any] = field(default_factory=list, repr=False)
    component: T.Any = None
    config: T.Any = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)


def _append(x, indent, result):
    result.append(" " * (indent) + x)


def render_elm(elm, result, level=0, url=""):
    wraps = elm.config and elm.config.wraps
    url_postfix = get_elm_url_postfix(elm)
    route_name = create_route_name() if ":" in url_postfix else None

    if url_postfix:
        url += f"/{url_postfix}"
        exact = "exact={true} " if not elm.children else ""
        name = f"name='{route_name}' " if route_name else ""
        _append(f'<Route {exact}{name}path="{url}">', level * 2, result)
        level += 1

    deps = []
    for dep_chain in elm.dep_chains:
        deps.extend(dep_chain)

    for dep in deps:
        if dep.wraps:
            _append(f"<{dep.component.typ.name} >", level * 2, result)
            level += 1

    for dep in deps:
        if not dep.wraps:
            _append(f"<{dep.component.typ.name} />", level * 2, result)

    if elm.component:
        component_postfix = "" if wraps else " /"
        _append(f"<{elm.component.typ.name}{component_postfix}>", level * 2, result)
        if wraps:
            level += 1

    for child_elm in elm.children:
        render_elm(child_elm, result, level + 1, url)

    if elm.component:
        if wraps:
            level -= 1
            _append(f"</{elm.component.typ.name}>", (level + 1) * 2, result)

    for dep in reversed(deps):
        if dep.wraps:
            level -= 1
            _append(f"</{dep.component.typ.name} >", (level + 1) * 2, result)

    if elm.config and elm.config.url:
        _append("</Route>", level * 2, result)
        level -= 1

    return result


def get_elm_url_postfix(elm):
    if not elm.config:
        return ""

    params = elm.config.params
    for dep_chain in elm.dep_chains:
        for dep in dep_chain:
            for param in [f":{x}" for x in dep.params]:
                if param not in params:
                    params.append(param)
    return elm.config.url + join("/", "/".join(params))


def _create_dep_chain(dep_router_configs):
    result = []
    for router_config in dep_router_configs:
        result.append(router_config)
        for side_effect in router_config.side_effects:
            result.append(side_effect)
    return result


def add_child_elm(elm, elm_component):
    child_elm = Elm(component=elm_component)
    elm.add_child(child_elm)

    q = Queue(lambda x: x, [elm_component])
    for embedded_component in q:
        router_configs = embedded_component.typ.create_router_configs(
            embedded_component
        )
        if embedded_component is elm_component:
            child_elm.config = router_configs[-1] if router_configs else None
        dep_route_configs = router_configs[:-1]
        if dep_route_configs:
            child_elm.dep_chains.append(_create_dep_chain(dep_route_configs))
        q.extend(embedded_component.typ.child_components)

    return child_elm


def _get_root_elm(modules):
    root_components = []
    for module in modules:
        root_components.extend(module.routed_components)

    root = Elm(config=None)
    q = Queue(lambda x: x, [root])
    for elm in q:
        components = (
            root_components if elm is root else elm.component.wrapped_components
        )
        for wrapped_component in components:
            child_elm = add_child_elm(elm, wrapped_component)
            q.append(child_elm)

    return root


def _components_used_in_router(root):
    result = []

    def add(component):
        if component not in result:
            result.append(component.typ)

    q = Queue(lambda x: x, [root])
    for elm in q:
        if elm is not root:
            add(elm.component)
            for dep_chain in elm.dep_chains:
                for dep in dep_chain:
                    add(dep.component)
        q.extend(elm.children)

    return result


def _equal_dep(lhs, rhs):
    return lhs.component.typ is rhs.component.typ


def _prune_dep_chains(root):
    q = Queue(lambda x: x, [root])
    for elm in q:
        dep_chains = list(sorted(elm.dep_chains, key=lambda x: len(x)))
        elm.dep_chains.clear()
        for dep_chain in dep_chains:
            pruned_chain = []
            for dep in dep_chain:
                skip = False
                other_elm = elm
                while other_elm:
                    for other_dep_chain in other_elm.dep_chains:
                        if other_dep_chain == dep_chain:
                            continue
                        if [x for x in other_dep_chain if _equal_dep(x, dep)]:
                            skip = True
                            break
                    if skip:
                        break
                    else:
                        # TODO if other_elm disallows finding dep in a parent
                        # elm, then stop processing all further deps in this
                        # dep chain.
                        other_elm = other_elm.parent
                if not skip:
                    pruned_chain.append(dep)

            if pruned_chain:
                elm.dep_chains.append(pruned_chain)
        q.extend(elm.children)


def get_context(router):
    _ = lambda: None
    _.react_app = ml_react_app(router)
    _.root = _get_root_elm(_.react_app.modules)
    _prune_dep_chains(_.root)

    class Sections:
        def route_imports(self):
            used_components = _components_used_in_router(_.root)

            result = []
            imports_by_module_name = R.group_by(
                lambda x: x.module.name, used_components
            )
            for module_name, components in imports_by_module_name.items():
                component_names = ", ".join(R.map(lambda x: x.name)(components))
                result.append(
                    f"import {{ {component_names} }} from 'src/{module_name}/components';"
                )
            return os.linesep.join(result)

        def routes(self):
            result = []
            render_elm(_.root, result)
            return os.linesep.join(result)

    return dict(sections=Sections())
