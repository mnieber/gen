def _modules(self):
    return [x for x in self.django_app.modules if x.item_types]


def p_section_base_classes(self):
    return "".join([f"{x.name_snake}.schema.Query, " for x in _modules(self)])


def p_section_imports(self):
    return "\n".join([f"import {x.name_snake}.schema" for x in _modules(self)])
