from moonleap import upper0


def imports_section(self):
    facet_name = upper0(self.term.tag)
    return (
        f"import {{ {facet_name}, {facet_name}Cbs }} from 'skandha-facets/{facet_name}'"
    )


def constructor_section(self):
    facet_name = upper0(self.name)
    return f"  @facet {self.name}: {facet_name} = new {facet_name}();"


def callbacks_section(self):
    return ""


def declare_policies_section(self):
    return ""


def policies_section(self):
    return ""
