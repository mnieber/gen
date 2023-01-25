from titan.react_view_pkg.pkg.add_div import add_div_open
from titan.react_view_pkg.pkg.builder import Builder


class ImageBuilder(Builder):
    type = "Image"

    def build(self):
        url = self.get_value("url")
        self.widget_spec.div.elm = "img"
        self.widget_spec.div.append_attrs(['alt=""', f'src="{url}"'])
        add_div_open(self, also_close=True)
