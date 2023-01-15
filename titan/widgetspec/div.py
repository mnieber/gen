import typing as T
from dataclasses import dataclass, field

from titan.widgetspec.sort_styles import sort_styles


@dataclass
class Div:
    styles: T.List[str] = field(repr=True, default_factory=list)
    attrs: T.List[str] = field(repr=False, default_factory=list)
    key: T.Optional[str] = None

    def prepend_styles(self, styles):
        for style in reversed(styles):
            if style not in self.styles:
                self.styles.insert(0, style)

    def append_styles(self, styles):
        for style in styles:
            if style not in self.styles:
                self.styles.append(style)

    def append_attrs(self, attrs):
        for attr in attrs:
            if attr not in self.attrs:
                self.attrs.append(attr)

    def get_class_name_attr(self, widget_class_name=None):
        prefix = [f'"{widget_class_name}"'] if widget_class_name else []
        infix = list(self.styles)

        suffix = []
        if "props.className" in self.styles:
            suffix += ["props.className"]
            infix.remove("props.className")

        if prefix or infix or suffix:
            styles_str = ", ".join(prefix + sort_styles(infix + suffix))
            return f"className={{ cn({styles_str}) }}"
        return ""
