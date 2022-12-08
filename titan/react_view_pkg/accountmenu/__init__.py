from moonleap import create
from titan.react_pkg.component import Component

base_tags = {"menu": ["component"]}


@create("account-:menu")
def create_account_menu(term):
    component = Component(name="AccountMenu")
    return component
