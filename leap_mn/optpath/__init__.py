import moonleap.props as P
import ramda as R
from moonleap import Prop, extend
from moonleap.memfun import MemFun
from moonleap.rel import Rel
from moonleap.slctrs import Selector
from moonleap.utils.inflect import singular_noun

from . import props
from .resources import OptPath


def tree_prop(verb, term, merge, initial):
    rdcr = R.reduce(merge, initial)
    chain = R.chain(R.identity)
    children_prop = P.children(verb, term)
    sources_prop = P.children(verb, f"{singular_noun(term)}-sources")

    def get_value(parent):
        class Inner:
            @property
            def merged(self):
                return rdcr(
                    self.children
                    + chain([children_prop.get_value(x) for x in self.sources])
                )

            @property
            def children(self):
                return children_prop.get_value(parent)

            @property
            def sources(self):
                return sources_prop.get_value(parent)

            def add(self, child):
                children_prop.add_value(parent, child)

            def add_source(self, source):
                sources_prop.add_value(parent, source)

        return Inner()

    return Prop(get_value)


class StoreOptPaths:
    opt_paths = tree_prop(
        "has", "opt-path", merge=lambda acc, x: [*acc, x], initial=list()
    )
