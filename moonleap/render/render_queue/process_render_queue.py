from moonleap.render.render_queue.render_queue import RenderQueueTask, get_render_queue


def process_render_queue():
    render_queue = get_render_queue()
    while len(render_queue) > 0:
        task = render_queue.pop()
        _render(task)


def _render(task: RenderQueueTask):
    pass
