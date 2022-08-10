from moonleap import create, create_forward, rule
from moonleap.verbs import has
from titan.react_pkg.component import Component

base_tags = [("menu", ["component"])]


@create("account:menu")
def create_account_menu(term):
    component = Component(name="accountMenu")
    return component


@rule("account:menu")
def created_account_menu(account_menu):
    return create_forward("auth:module", has, account_menu)
