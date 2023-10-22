import typing as T

from dataclassy import dataclass


@dataclass
class RenderQueueTask:
    path: str
    context: []
    helpers: dict = {}
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
