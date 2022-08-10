import os
from pathlib import Path

import markdown
from moonleap.render.render_template import render_template
from moonleap.session import get_session


def _fn(resource, report_dir):
    id = resource.id
    report_basename = id + ".html"
    return os.path.join(report_dir, report_basename)


def report_resources(blocks):
    report_dir = ".moonleap/report"
    index_fn = os.path.abspath(os.path.join(report_dir, "index.html"))

    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    for block in blocks:
        resource_by_term = [x for x in block.get_resource_by_term() if x[2]]
        for term, resource, is_owner in resource_by_term:
            report_fn = _fn(resource, report_dir)
            with open(report_fn, "w") as ofs:
                ofs.write(create_report(resource, term, index_fn))

    with open(index_fn, "w") as ofs:
        ofs.write(create_index(blocks))


def create_report(resource, term, index_fn):
    default_template_fn = Path(__file__).parent / "templates" / "resource.md.j2"
    body = render_template(
        default_template_fn,
        term=term,
        settings=get_session().settings,
        props={},
        child_relations=resource.get_relations(),
        parent_relations=resource.get_inv_relations(),
        index_fn=index_fn,
        res=resource,
    )
    return (
        "<html><body>"
        + f"""{markdown.markdown(body, extensions=['tables'])}"""
        + "</body></html>"
    )


def create_index(blocks):
    template_fn = Path(__file__).parent / "templates" / "index.md.j2"

    resource_by_term_str = {}
    root_block = blocks[0]
    for block in root_block.get_blocks(include_children=True):
        for term, resource, is_owner in block.get_resource_by_term():
            if is_owner:
                resource_by_term_str[str(term)] = resource

    body = render_template(
        template_fn,
        settings=get_session().settings,
        resource_by_term_str=sorted(
            list(resource_by_term_str.items()), key=lambda x: x[0]
        ),
    )
    return (
        "<html><body>"
        + f"""{markdown.markdown(body, extensions=['tables'])}"""
        + "</body></html>"
    )
