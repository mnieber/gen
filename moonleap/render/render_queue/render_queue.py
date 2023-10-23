import typing as T
from argparse import Namespace

from dataclassy import dataclass
from moonleap.render.root_resource import get_root_resource


@dataclass
class RenderQueueTask:
    templates_dir: str
    output_path: str
    context: Namespace
    get_helpers: T.Callable
    get_meta_data_by_fn: T.Callable
    parent_task: "RenderQueueTask"
    _helpers = None

    @property
    def helpers(self):
        if self._helpers:
            return self._helpers
        if self.get_helpers:
            self._helpers = self.get_helpers(_=self.context)
            return self._helpers
        elif self.parent_task:
            return self.parent_task.helpers
        return dict()

    @property
    def meta_data_by_fn(self):
        if self.get_meta_data_by_fn:
            return self.get_meta_data_by_fn(_=self.context, __=self.helpers)
        return dict()


class RenderQueue:
    def __init__(self):
        self.queue = []

    def add(self, task):
        for i in range(len(self.queue)):
            if self.queue[i].parent_task != task.parent_task:
                self.queue.insert(i, task)
                return
        self.queue.append(task)

    def pop(self):
        return self.queue.pop(0)

    def __len__(self):
        return len(self.queue)


_render_queue = RenderQueue()


def get_render_queue():
    return _render_queue


_root_render_task = None


def get_root_render_task():
    from moonleap.session import get_session

    global _root_render_task
    if _root_render_task is None:
        _root_render_task = RenderQueueTask(
            templates_dir="",
            output_path=".",
            context=Namespace(
                settings=get_session().settings, root_resource=get_root_resource()
            ),
            get_helpers=None,
            get_meta_data_by_fn=lambda: dict(),
            parent_task=None,
        )
    return _root_render_task
