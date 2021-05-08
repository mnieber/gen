import os
from pathlib import Path

import markdown
from moonleap.parser.term import term_to_word
from moonleap.render.template_renderer import _render
from moonleap.resource.rel import fuzzy_match


def _fn(resource, report_dir):
    id = resource.id
    report_basename = id + ".html"
    return os.path.join(report_dir, report_basename)


def _get_relations(res, is_inv):
    return [
        (rel, other_res)
        for rel, other_res in res._relations
        if rel.is_inv == is_inv
        # below we check if the rel is not in the private rels of the parent
        and (
            # first case (not is_inv): res is the parent and other_res is the child
            (not is_inv and not _match_rel_to_rels(rel, res.doc_meta.private_rels))
            # second case (is_inv): the opposite
            or (
                is_inv
                and not _match_rel_to_rels(rel.inv(), other_res.doc_meta.private_rels)
            )
        )
    ]


def _match_rel_to_rels(rel, other_rels):
    for other_rel in other_rels:
        if fuzzy_match(rel, other_rel):
            return True
    return False


def report_resources(blocks, settings, output_root_dir):
    report_dir = os.path.join(output_root_dir, ".report")

    if not os.path.exists(report_dir):
        os.mkdir(report_dir)

    for block in blocks:
        resources = [x for x in block.get_resources() if x.block == block]
        for resource in resources:
            if hasattr(resource.__class__, "doc_meta"):
                resource.doc_meta.add(resource.__class__.doc_meta)
            report_file = _fn(resource, report_dir)
            with open(report_file, "w") as ofs:
                ofs.write(create_report(resource, settings))


def create_report(resource, settings):
    default_template_fn = Path(__file__).parent / "templates" / "resource.md.j2"
    props = {
        prop_name: getattr(resource, prop_name) for prop_name in resource.doc_meta.props
    }
    child_relations = [
        (rel, res) for (rel, res) in _get_relations(resource, is_inv=False) if rel.subj
    ]
    parent_relations = [
        (rel, res) for (rel, res) in _get_relations(resource, is_inv=True) if rel.subj
    ]
    body = _render(
        default_template_fn,
        resource,
        settings=settings,
        props=props,
        child_relations=child_relations,
        parent_relations=parent_relations,
    )
    return f"""<html><body>{markdown.markdown(body, extensions=['tables'])}</body></html>"""
