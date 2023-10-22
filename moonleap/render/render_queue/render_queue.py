import typing as T

from dataclassy import dataclass
from moonleap.render.root_resource import get_root_resource


@dataclass
class RenderQueueTask:
    path: str
    context: []
    get_helpers: T.Callable
    get_meta_data_by_fn: T.Callable
    parent_task: "RenderQueueTask"

    @property
    def parent_helpers(self):
        return None if self.parent_task is None else self.parent_task.helpers


class RenderQueue:
    def __init__(self):
        self.queue = []

    def add(self, task):
        self.queue.append(task)

    def pop(self):
        return self.queue.pop(0)

    def __len__(self):
        return len(self.queue)


_render_queue = RenderQueue()


def get_render_queue():
    return _render_queue


_root_render_task = RenderQueueTask(
    path=".",
    context=[get_root_resource()],
    parent_task=None,
    get_helpers=lambda: dict(),
    get_meta_data_by_fn=lambda: dict(),
)


def get_root_render_task():
    return _root_render_task
