from pathlib import Path

from moonleap.render.render_queue.add_render_tasks import add_render_tasks
from moonleap.render.render_queue.render_queue import RenderQueueTask, get_render_queue
from moonleap.render.render_template import render_template
from moonleap.session import get_session


def process_render_queue():
    render_queue = get_render_queue()
    while len(render_queue) > 0:
        task = render_queue.pop()
        _render(task)


def _render(task: RenderQueueTask):
    helpers = task.helpers
    meta_data_by_fn = task.meta_data_by_fn

    template_fns = [x for x in Path(task.templates_dir).glob("*") if not _exclude(x)]
    for template_fn in template_fns:
        meta_data = meta_data_by_fn.get(template_fn.name, dict())
        if not meta_data.get("include", True):
            continue

        output_fn = _get_output_fn(task.output_path, template_fn, meta_data)
        if template_fn.is_dir():
            add_render_tasks(template_fn, output_fn, task)
        else:
            get_session().file_writer.write_file(
                output_fn,
                content=render_template(template_fn, dict(_=task.context, __=helpers)),
                is_dir=False,
            )


def _get_output_fn(output_path, template_fn, meta_data):
    name = meta_data["name"] if "name" in meta_data else template_fn.name

    if name.endswith(".j2"):
        name = name[:-3]

    return Path(output_path) / name


def _exclude(fn):
    return fn.name.startswith("__moonleap__") or fn.name == "__pycache__"
