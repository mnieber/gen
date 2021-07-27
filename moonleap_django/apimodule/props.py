def _modules(self):
    # TODO return modules that have a schema
    return []


def p_section_base_classes(self):
    return ", ".join([f"{x.name_snake}.schema.Query" for x in _modules(self)])


def p_section_imports(self):
    return "\n".join([f"import {x.name_snake}.schema" for x in _modules(self)])
