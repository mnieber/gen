from pathlib import Path

import ramda as R
from moonleap.parser.term import maybe_term_to_term
from moonleap.resource.prop import Prop
from moonleap.resource.rel import Rel
from moonleap.resource.slctrs import Selector

from .resources import OutputPath


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

    def update_doc_meta(prop_name, doc_meta):
        doc_meta.doc_prop(prop_name)

    return Prop(
        get_value=get_child, set_value=set_child, update_doc_meta=update_doc_meta
    )


def merged_output_path():
    def _merge(acc, x):
        return OutputPath(location=(x.location + acc.location))

    def get_value(resource):
        return Path(
            R.reduce(_merge, OutputPath(""), resource.output_paths.merged).location
        )

    def update_doc_meta(prop_name, doc_meta):
        doc_meta.doc_prop(prop_name)

    return Prop(get_value=get_value, update_doc_meta=update_doc_meta)
