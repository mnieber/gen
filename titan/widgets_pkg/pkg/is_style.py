import re

style_patterns = [
    r"text-(.+)-([0-9]+)",
    r"bg-(.+)-([0-9]+)",
    r"p-([0-9]+)",
    r"px-([0-9]+)",
    r"py-([0-9]+)",
    r"m-([0-9]+)",
    r"mx-([0-9]+)",
    r"my-([0-9]+)",
    r"mt-([0-9]+)",
    r"mb-([0-9]+)",
    r"rounded",
    r"rounded-(.+)",
    r"flex",
    r"flex-col",
    r"flex-row",
    r"justify-end",
    r"justify-start",
]


def is_style(part):
    for style_pattern in style_patterns:
        if re.fullmatch(style_pattern, part):
            return True
    return False
