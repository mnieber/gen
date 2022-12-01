from titan.react_view_pkg.pkg.builder import Builder


class ChildrenBuilder(Builder):
    def build(self, div_attrs=None):
        self.add_lines(["{props.children}"])
