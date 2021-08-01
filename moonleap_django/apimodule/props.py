def _modules(self):
    return [x for x in self.django_app.modules if x.item_types]


def p_section_base_classes(self, postfix):
    result = "".join([f"{x.name_snake}.schema.{postfix}, " for x in _modules(self)])
    return (result + "graphene.ObjectType") if result else ""


def p_section_imports(self):
    return "\n".join([f"import {x.name_snake}.schema" for x in _modules(self)])
