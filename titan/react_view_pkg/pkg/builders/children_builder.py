from titan.react_view_pkg.pkg.builder import Builder


class ChildrenBuilder(Builder):
    type = "Children"

    def build(self):
        self.output.add(lines=["{props.children}"])
