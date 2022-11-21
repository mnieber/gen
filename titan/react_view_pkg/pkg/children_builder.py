from titan.react_view_pkg.pkg.builder import Builder


class ChildrenBuilder(Builder):
    def build(self, classes=None, handlers=None):
        self += ["{props.children}"]
