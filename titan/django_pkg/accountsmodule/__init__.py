from pathlib import Path

from moonleap import create, kebab_to_camel
from moonleap.utils.case import sn

from .resources import AccountsModule  # noqa


@create("accounts:module")
def accounts_module_created(term):
    name = kebab_to_camel(term.data)
    module = AccountsModule(name=name)
    module.add_template_dir(Path(__file__).parent / "templates")
    module.output_path = sn(module.name)
    return module
