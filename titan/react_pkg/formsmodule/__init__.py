from moonleap import rule


@rule("forms:module")
def forms_module_created(forms_module):
    forms_module.react_app.get_module("utils").use_packages(
        ["useScheduledCall", "ValuePicker", "slugify"]
    )
