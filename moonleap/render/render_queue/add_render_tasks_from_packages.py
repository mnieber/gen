import os

from moonleap.packages.scope_manager import import_package
from moonleap.render.render_queue.render_queue import RenderQueueTask, get_render_queue
from moonleap.render.root_resource import get_root_resource


def add_render_tasks_from_packages(packages_by_scope):
    for scope, package_names in packages_by_scope.items():
        for package_name in package_names:
            package = import_package(package_name)
            template_dir = os.path.join(package.__path__[0], "templates")
            if os.path.exists(template_dir):
                get_render_queue().add(
                    RenderQueueTask(
                        path=template_dir,
                        context=[get_root_resource()],
                        parent_task=None,
                    )
                )
