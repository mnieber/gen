import typing as T
from dataclasses import dataclass, field

from titan.widgetspec.sort_styles import maybe_quote_style, sort_styles


@dataclass
class Div:
    _elm: str = ""
    styles: T.List[str] = field(repr=True, default_factory=list)
    attrs: T.List[str] = field(repr=False, default_factory=list)
    key: T.Optional[str] = None

    @property
    def elm(self):
        return self._elm or "div"

    @elm.setter
    def elm(self, x):
        self._elm = x

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
        prefix = [widget_class_name] if widget_class_name else []

        if prefix or self.styles:
            quoted_styles = [
                maybe_quote_style(x) for x in prefix + sort_styles(self.styles)
            ]
            styles_str = ", ".join(quoted_styles)
            return f"className={{ cn({styles_str}) }}"
        return ""
