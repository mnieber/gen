import fnmatch

from moonleap.utils.quote import quote, quote_all
from titan.widgetspec.is_style import normalize_style

style_order = [
    (["card", "rowSkewer", "colSkewer", "button", "bigButton"], False),
    (["grid", "grid-*", "flex", "flex-*", "items-*", "justify-*"], True),
    (["m-*", "mt-*", "mb-*", "ml-*", "mr-*", "mx-*", "my-*"], True),
    (["p-*", "pt-*", "pb-*", "pl-*", "pr-*", "px-*", "py-*"], True),
    (["*"], False),
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
            for pattern in quote_all(group) if is_quoted else group:
                if fnmatch.fnmatch(normalize_style(style), pattern):
                    unquoted_style = style[1:-1] if is_quoted else style
                    group_styles.append(unquoted_style)
                    unused_styles.remove(style)
                    break

        if group_styles:
            if group == ["*"]:
                result += group_styles
            else:
                sep = " " if is_quoted else ", "
                style = sep.join(group_styles)
                if is_quoted:
                    style = quote(style)
                result.append(style)

    return result
