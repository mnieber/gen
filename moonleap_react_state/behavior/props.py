from moonleap import upper0


def p_section_imports(self):
    facet_name = upper0(self.name)
    return (
        f"import {{ {facet_name}, {facet_name}Cbs }} "
        + f"from 'skandha-facets/{facet_name}';"
    )


def p_section_constructor(self):
    facet_name = upper0(self.name)
    return f"  {self.name}: new {facet_name}(),"


def p_section_callbacks(self, bvrs):
    return ""


def p_section_declare_policies(self, bvrs):
    return ""


def p_section_policies(self, bvrs):
    return ""


def p_section_default_props(self, store):
    return ""
