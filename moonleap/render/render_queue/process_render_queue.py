from moonleap.render.render_queue.render_queue import RenderQueueTask, get_render_queue
from moonleap.render.render_templates.create_render_helpers import create_render_helpers


def process_render_queue():
    render_queue = get_render_queue()
    while len(render_queue) > 0:
        task = render_queue.pop()
        _render(task)


def _render(task: RenderQueueTask):
    task.helpers, render_in_context, meta_data_by_fn = create_render_helpers(
        task.path, task.context, prev_helpers=task.parent_helpers
    )
