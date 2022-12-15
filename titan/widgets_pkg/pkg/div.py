import typing as T
from dataclasses import dataclass, field


@dataclass
class Div:
    styles: T.List[str] = field(repr=False, default_factory=list)
    attrs: T.List[str] = field(repr=False, default_factory=list)
    key: T.Optional[str] = None

    def prepend_styles(self, styles):
        for style in reversed(styles):
            if style not in self.styles:
                self.styles.insert(0, style)

    def append_styles(self, styles):
        for style in reversed(styles):
            if style not in self.styles:
                self.styles.append(style)

    @property
    def class_name_attr(self):
        if self.styles:
            styles_str = " ".join(self.styles)
            return f"className={{ cn({styles_str}) }}"
        return None
