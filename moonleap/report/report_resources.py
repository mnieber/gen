import os
from pathlib import Path

import markdown
from moonleap.parser.term import term_to_word
from moonleap.render.template_renderer import _render


def _fn(resource, report_dir):
    id = resource.id
    report_basename = id + ".html"
    return os.path.join(report_dir, report_basename)


def report_resources(blocks, settings, output_root_dir):
    report_dir = os.path.join(output_root_dir, ".report")

    if not os.path.exists(report_dir):
        os.mkdir(report_dir)

    for block in blocks:
        resources = [x for x in block.get_resources() if x.block == block]
        for resource in resources:
            report_file = _fn(resource, report_dir)
            with open(report_file, "w") as ofs:
                ofs.write(create_report(resource, settings))


def create_report(resource, settings):
    default_template_fn = Path(__file__).parent / "templates" / "resource.md.j2"
    body = _render(default_template_fn, resource, settings)
    return f"""<html><body>{markdown.markdown(body, extensions=['tables'])}</body></html>"""
