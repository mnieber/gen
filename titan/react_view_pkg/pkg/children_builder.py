from titan.react_view_pkg.pkg.builder import Builder


class ChildrenBuilder(Builder):
    def get_div(self, classes=None):
        self += ["{props.children}"]

        return self._output()
