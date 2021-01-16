from moonleap.parser.term import maybe_term_to_term
from moonleap.resource.prop import Prop
from moonleap.resource.rel import Rel
from moonleap.resource.slctrs import Selector

from .resources import OutputPath


def merge(acc, x):
    return OutputPath(location=(x.location + acc.location))


def output_path(verb, term):
    rel = Rel(verb=verb, obj=maybe_term_to_term(term))
    slctr = Selector([rel])

    def get_child(self):
        children = slctr.select_from(self)
        if len(children) > 1:
            raise Exception(f"More than 1 child, verb={verb}, term={term}")

        return None if not children else children[0].location

    def set_child(self, output_path):
        children = slctr.select_from(self)
        if len(children) > 0:
            raise Exception("Already has a child")

        child = OutputPath(output_path)
        child.block = self.block
        child.term = self.term
        self.add_relation(rel, child)

    return Prop(get_value=get_child, set_value=set_child)
