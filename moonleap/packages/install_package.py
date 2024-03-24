from moonleap.extension.extend import apply_extension
from moonleap.packages.get_module_symbols import get_module_symbols
from moonleap.render.file_merger import add_file_merger
from moonleap.templates.template_env import add_filter
from moonleap.templates.transforms import register_transforms


def install_package(package):
    for module in getattr(package, "modules", []):
        install_module(module)


def install_module(module):
    extensions = []

    for f in get_module_symbols(module):
        if hasattr(f, "moonleap_extends_resource_type"):
            extensions.append(f)

    if hasattr(module, "meta"):
        if extensions:
            raise Exception(
                "Extensions should either be created in the module "
                + f"or in the meta function, not both.\nIn module: {module}"
            )
        extensions = module.meta()

    register_transforms(
        getattr(module, "transforms", []),
        getattr(module, "post_transforms", []),
    )

    for file_merger in getattr(module, "file_mergers", []):
        add_file_merger(file_merger)

    for name, f in getattr(module, "filters", {}).items():
        add_filter(name, f)

    for extension in extensions:
        resource_type = extension.moonleap_extends_resource_type
        apply_extension(resource_type, extension)
