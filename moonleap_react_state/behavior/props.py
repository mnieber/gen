from moonleap import upper0


def imports_section(self):
    facet_name = upper0(self.name)
    return (
        f"import {{ {facet_name}, {facet_name}Cbs }} "
        + f"from 'skandha-facets/{facet_name}';"
    )


def constructor_section(self):
    facet_name = upper0(self.name)
    return f"  {self.name}: new {facet_name}(),"


def callbacks_section(self, bvrs):
    return ""


def declare_policies_section(self, bvrs):
    return ""


def policies_section(self, bvrs):
    return ""


def default_props_section(self, store):
    return ""
