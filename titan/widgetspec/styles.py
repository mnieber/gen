import re
import typing as T

from dataclassy import dataclass


@dataclass
class StylePattern:
    group: str
    is_quoted: bool
    is_scss: bool
    is_tailwind: bool
    pattern: str
    scss_imports: T.List[str] = []

    def match(self, style):
        pattern = self.pattern.replace("*", "(.*)")
        return re.fullmatch(pattern, normalize_style(style))


SP = StylePattern

font_sizes_import = '@import "src/frames/styles/font-sizes.scss";'

# fmt: off
style_patterns = [
    SP(group="mixins", is_quoted=0, is_scss=0, is_tailwind=0, pattern="card"),
    SP(group="mixins", is_quoted=0, is_scss=0, is_tailwind=0, pattern="rowSkewer"),
    SP(group="mixins", is_quoted=0, is_scss=0, is_tailwind=0, pattern="colSkewer"),
    SP(group="mixins", is_quoted=0, is_scss=0, is_tailwind=0, pattern="rowBanner"),
    SP(group="mixins", is_quoted=0, is_scss=0, is_tailwind=0, pattern="colBanner"),
    SP(group="mixins", is_quoted=0, is_scss=0, is_tailwind=0, pattern="button"),
    SP(group="mixins", is_quoted=0, is_scss=0, is_tailwind=0, pattern="bigButton"),
    SP(group="layout", is_quoted=1, is_scss=0, is_tailwind=0, pattern="grid"),
    SP(group="layout", is_quoted=1, is_scss=0, is_tailwind=0, pattern="grid-*"),
    SP(group="layout", is_quoted=1, is_scss=0, is_tailwind=0, pattern="flex"),
    SP(group="layout", is_quoted=1, is_scss=0, is_tailwind=0, pattern="flex-*"),
    SP(group="layout", is_quoted=1, is_scss=0, is_tailwind=0, pattern="items-*"),
    SP(group="layout", is_quoted=1, is_scss=0, is_tailwind=0, pattern="justify-*"),
    SP(group="layout", is_quoted=1, is_scss=0, is_tailwind=0, pattern="self-*"),
    SP(group="margins", is_quoted=1, is_scss=0, is_tailwind=1, pattern="m-*"),
    SP(group="margins", is_quoted=1, is_scss=0, is_tailwind=1, pattern="mt-*"),
    SP(group="margins", is_quoted=1, is_scss=0, is_tailwind=1, pattern="mb-*"),
    SP(group="margins", is_quoted=1, is_scss=0, is_tailwind=1, pattern="ml-*"),
    SP(group="margins", is_quoted=1, is_scss=0, is_tailwind=1, pattern="mr-*"),
    SP(group="margins", is_quoted=1, is_scss=0, is_tailwind=1, pattern="mx-*"),
    SP(group="margins", is_quoted=1, is_scss=0, is_tailwind=1, pattern="my-*"),
    SP(group="paddings", is_quoted=1, is_scss=0, is_tailwind=1, pattern="p-*"),
    SP(group="paddings", is_quoted=1, is_scss=0, is_tailwind=1, pattern="pt-*"),
    SP(group="paddings", is_quoted=1, is_scss=0, is_tailwind=1, pattern="pb-*"),
    SP(group="paddings", is_quoted=1, is_scss=0, is_tailwind=1, pattern="pl-*"),
    SP(group="paddings", is_quoted=1, is_scss=0, is_tailwind=1, pattern="pr-*"),
    SP(group="paddings", is_quoted=1, is_scss=0, is_tailwind=1, pattern="px-*"),
    SP(group="paddings", is_quoted=1, is_scss=0, is_tailwind=1, pattern="py-*"),
    SP(group="sizes", is_quoted=1, is_scss=1, is_tailwind=1, pattern="h-*"),
    SP(group="sizes", is_quoted=1, is_scss=1, is_tailwind=1, pattern="w-*"),
    SP(group="sizes", is_quoted=1, is_scss=1, is_tailwind=1, pattern="min-w-*"),
    SP(group="sizes", is_quoted=1, is_scss=1, is_tailwind=1, pattern="max-w-*"),
    SP(group="other", is_quoted=1, is_scss=1, is_tailwind=0, pattern="text-(xxs|xs|sm|md|l|xl|xxl)", scss_imports=[font_sizes_import]),
    SP(group="other", is_quoted=1, is_scss=1, is_tailwind=1, pattern="text-*"),
    SP(group="other", is_quoted=1, is_scss=1, is_tailwind=0, pattern="title-*", scss_imports=[font_sizes_import]),
    SP(group="other", is_quoted=1, is_scss=1, is_tailwind=1, pattern="bg-*"),
    SP(group="other", is_quoted=1, is_scss=1, is_tailwind=1, pattern="rounded-*"),
    SP(group="className", is_quoted=0, is_scss=0, is_tailwind=0, pattern="props.className"),
]
# fmt: on


def normalize_style(style):
    return style.replace("!", "")


def is_style(part):
    for group in get_style_groups():
        for pattern in group:
            if pattern.match(part):
                return True
    return False


_styles_by_group = {}


def get_style_groups():
    if _styles_by_group:
        return _styles_by_group.values()

    for style_pattern in style_patterns:
        styles = _styles_by_group.setdefault(style_pattern.group, [])
        styles.append(style_pattern)

    return _styles_by_group.values()
