def _modules(self):
    return [x for x in self.django_app.modules if x.item_types]


class Sections:
    def __init__(self, res):
        self.res = res

    def base_classes(self, postfix):
        result = "".join(
            [f"{x.name_snake}.schema.{postfix}, " for x in _modules(self.res)]
        )
        return (result + "graphene.ObjectType") if result else ""

    def imports(self):
        return "\n".join([f"import {x.name_snake}.schema" for x in _modules(self.res)])
