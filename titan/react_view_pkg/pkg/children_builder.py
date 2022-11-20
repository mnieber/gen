from titan.react_view_pkg.pkg.builder import Builder


class ChildrenBuilder(Builder):
    def build(self, classes=None):
        self += ["{props.children}"]
