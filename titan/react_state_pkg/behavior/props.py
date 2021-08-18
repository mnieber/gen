from moonleap import upper0


class Sections:
    def __init__(self, res):
        self.res = res

    def imports(self):
        facet_name = upper0(self.res.name)
        return (
            f"import {{ {facet_name}, {facet_name}Cbs }} "
            + f"from 'skandha-facets/{facet_name}';"
        )

    def constructor(self):
        facet_name = upper0(self.res.name)
        return f"  {self.res.name}: new {facet_name}(),"

    def callbacks(self, bvrs):
        return ""

    def declare_policies(self, bvrs):
        return ""

    def policies(self, bvrs):
        return ""

    def default_props(self, store):
        return ""
