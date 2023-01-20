from titan.react_view_pkg.pkg.builder import Builder


class ImageBuilder(Builder):
    def build(self):
        url = self.widget_spec.values["url"]
        self.widget_spec.div.elm = "img"
        self.widget_spec.div.append_attrs(['alt=""', f'src="{url}"'])
        self._add_div_open(also_close=True)
