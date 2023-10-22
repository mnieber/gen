from argparse import Namespace

from moonleap.render.render_queue.render_queue import RenderQueueTask, get_render_queue
from moonleap.render.render_templates.create_render_helpers import create_render_helpers


def add_render_tasks(templates_dir, output_path, parent_render_task):
    (
        get_helpers,
        get_meta_data_by_fn,
        get_contexts,
    ) = create_render_helpers(
        templates_dir,
    )

    context_extentions = (
        get_contexts(parent_render_task.context) if get_contexts else [{}]
    )
    for context_extention in context_extentions:
        full_context = Namespace(
            **parent_render_task.context.__dict__, **context_extention
        )
        get_render_queue().add(
            RenderQueueTask(
                templates_dir=templates_dir,
                output_path=output_path,
                context=full_context,
                parent_task=parent_render_task,
                get_helpers=get_helpers,
                get_meta_data_by_fn=get_meta_data_by_fn,
            )
        )
