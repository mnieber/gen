import fnmatch

from moonleap.utils.quote import quote
from titan.widgetspec.is_style import normalize_style

style_order = [
    (["card", "rowSkewer", "colSkewer", "button", "bigButton"], False),
    (["grid", "grid-*", "flex", "flex-*", "items-*", "justify-*"], True),
    (["m-*", "mt-*", "mb-*", "ml-*", "mr-*", "mx-*", "my-*"], True),
    (["p-*", "pt-*", "pb-*", "pl-*", "pr-*", "px-*", "py-*"], True),
    (["*"], True),
    (["props.className"], False),
]


def sort_styles(styles):
    # Sort styles by order of appearance in style_order.
    # Wildcards are matched using fnmatch.
    # We return a list of strings, such that styles that belong to the same group
    # are placed in the same string.

    result = []
    unused_styles = list(styles)

    for group, is_quoted in style_order:
        group_styles = []
        for style in list(unused_styles):
            if style == "props.className" and group == ["*"]:
                continue
            for pattern in group:
                if fnmatch.fnmatch(normalize_style(style), pattern):
                    group_styles.append(style)
                    unused_styles.remove(style)
                    break

        if group_styles:
            sep = " " if is_quoted else ", "
            result += [sep.join(group_styles)]

    return result


def maybe_quote_style(style):
    if style.startswith("{"):
        return style

    for group, is_quoted in style_order:
        if not is_quoted and group != ["*"]:
            for pattern in group:
                if fnmatch.fnmatch(normalize_style(style), pattern):
                    return style
    return quote(style)
