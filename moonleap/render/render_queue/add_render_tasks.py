from moonleap.render.render_queue.render_queue import RenderQueueTask, get_render_queue
from moonleap.render.render_templates.create_render_helpers import create_render_helpers


def add_render_tasks(templates_dir, parent_render_task):
    (
        get_helpers,
        get_meta_data_by_fn,
        get_contexts,
    ) = create_render_helpers(
        templates_dir,
    )

    if get_contexts:
        for context in get_contexts():
            full_context = {**parent_render_task.context, **context}
            get_render_queue().add(
                RenderQueueTask(
                    path=templates_dir,
                    context=full_context,
                    parent_task=parent_render_task,
                    get_helpers=get_helpers,
                    get_meta_data_by_fn=get_meta_data_by_fn,
                )
            )
