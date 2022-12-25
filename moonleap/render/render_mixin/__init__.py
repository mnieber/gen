import os
import typing as T
from dataclasses import dataclass, field
from pathlib import Path

from moonleap.render.render_templates import render_templates
from moonleap.resources.resource import Resource


def render_resource(res, write_file, output_path, context=None, template_dirs=None):
    if context is None:
        context = dict()

    for maybe_template_dir in template_dirs or []:
        template_dir = (
            maybe_template_dir(res)
            if callable(maybe_template_dir)
            else maybe_template_dir
        )
        if template_dir is not None:
            render_templates(
                template_dir,
                write_file,
                output_path,
                context=context,
                helpers=dict(),
            )

    for render_task in T.cast(T.List[RenderTask], getattr(res, "render_tasks", [])):
        resources = (
            render_task.resources()
            if callable(render_task.resources)
            else render_task.resources
        )
        for res in resources:
            extra_context = (
                render_task.context(res)
                if callable(render_task.context)
                else render_task.context
            )

            render_resource(
                res,
                write_file,
                os.path.join(output_path, render_task.output_path),
                context=dict(**context, **extra_context),
                template_dirs=render_task.template_dirs,
            )


@dataclass
class RenderTask:
    resources: T.Union[T.List[Resource], T.Callable[[], T.List[Resource]]]
    output_path: str
    context: dict
    template_dirs: list


@dataclass
class RenderMixin:
    render_tasks: list = field(
        default_factory=list, init=False, compare=False, repr=False
    )

    def renders(self, resources, output_path, context, template_dirs):
        render_task = RenderTask(
            resources=resources,
            output_path=output_path,
            context=context,
            template_dirs=template_dirs,
        )
        self.render_tasks.append(render_task)


@dataclass
class TemplateDirMixin:
    template_dir: T.Optional[Path] = field(default=None, init=False, repr=False)
    template_context: T.Union[dict, T.Callable] = field(
        default_factory=dict, init=False, repr=False
    )


class RootResource(RenderMixin, Resource):
    pass


_root_resource = None


def get_root_resource():
    global _root_resource
    if not _root_resource:
        _root_resource = RootResource()
    return _root_resource
