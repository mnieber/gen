from moonleap import upper0
from moonleap.resources.type_spec_store import type_spec_store


class Sections:
    def __init__(self, res):
        self.res = res

    def item_fields(self, item_name):
        type_spec = type_spec_store().get(upper0(item_name))
        return "\n".join(
            [f"  {x.name}: name: faker.name.findName()," for x in type_spec.field_specs]
        )


def get_context(self):
    return dict(sections=Sections(self))
