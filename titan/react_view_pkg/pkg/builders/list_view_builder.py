from titan.react_view_pkg.pkg.builder import Builder


def lvi_spec(lvi_name):
    return {
        f"ListViewItem with {lvi_name}": "pass",
    }


def lvi_component_spec(lvi_name):
    return {
        f"LviComponent with {lvi_name} as ListViewItem, Bar[p-2]": {
            "LeftSlot with LviFields": "pass",
            "RightSlot with LviButtons": "pass",
        },
    }


class ListViewBuilder(Builder):
    def get_spec_extension(self, places):
        lvi_name = lvi_name = (
            self.get_value_by_name("lvi-name") or self._get_default_lvi_name()
        )
        result = {}
        if "ListViewItem" not in places:
            result.update(lvi_spec(lvi_name))
        if "LviComponent" not in places:
            result.update(lvi_component_spec(lvi_name))
        return result

    def _get_default_lvi_name(self):
        default_lvi_name = self.widget_spec.root.widget_name
        if "-:" in default_lvi_name:
            default_lvi_name = default_lvi_name.replace("-:", "-") + "-item:view"
        else:
            pos = default_lvi_name.find(":")
            default_lvi_name = default_lvi_name[:pos] + "-item:view"
        return default_lvi_name
