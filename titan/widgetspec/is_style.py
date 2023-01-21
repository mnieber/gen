import re

style_patterns = [
    r"bg-(.+)-([0-9]+)",
    r"flex-col",
    r"flex-row",
    r"flex",
    r"h-(.+)",
    r"justify-center",
    r"justify-end",
    r"justify-self-start",
    r"justify-start",
    r"m-([0-9]+)",
    r"mb-([0-9]+)",
    r"ml-([0-9]+)",
    r"mr-([0-9]+)",
    r"mt-([0-9]+)",
    r"mx-([0-9]+)",
    r"my-([0-9]+)",
    r"mx-auto",
    r"my-auto",
    r"max-w-(.+)",
    r"min-w-(.+)",
    r"p-([0-9]+)",
    r"pb-([0-9]+)",
    r"pl-([0-9]+)",
    r"pr-([0-9]+)",
    r"pt-([0-9]+)",
    r"px-([0-9]+)",
    r"py-([0-9]+)",
    r"rounded-(.+)",
    r"rounded",
    r"self-start",
    r"self-stretch",
    r"text-(.+)-([0-9]+)",
    r"title-(.+)",
    r"text-(.+)",
]


def is_style(part):
    part = normalize_style(part)
    for style_pattern in style_patterns:
        if re.fullmatch(style_pattern, part):
            return True
    return False


def normalize_style(style):
    return style.replace("!", "")
