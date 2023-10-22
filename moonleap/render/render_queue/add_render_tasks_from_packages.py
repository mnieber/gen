import os

from moonleap.packages.scope_manager import import_package
from moonleap.render.render_queue.add_render_tasks import add_render_tasks
from moonleap.render.render_queue.render_queue import get_root_render_task


def add_render_tasks_from_packages(packages_by_scope):
    for scope, package_names in packages_by_scope.items():
        for package_name in package_names:
            package = import_package(package_name)
            template_dir = os.path.join(package.__path__[0], "templates")
            if os.path.exists(template_dir):
                add_render_tasks(template_dir, ".", get_root_render_task())
