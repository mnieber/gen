from pathlib import Path

from moonleap import create, create_forward, rule
from moonleap.render.storetemplatedirs import add_template_dir
from moonleap.verbs import has
from titan.react_pkg.component import Component

base_tags = [("menu", ["component"])]


@create("account:menu")
def create_account_menu(term, block):
    return Component(name="accountMenu")


@rule("account:menu")
def created_account_menu(account_menu):
    return create_forward("auth:module", has, account_menu)


@rule("auth:module", has, "account:menu")
def auth_module_has_account_menu(auth_module, account_menu):
    auth_module.add_template_dir(Path(__file__).parent / "templates_auth_module")
