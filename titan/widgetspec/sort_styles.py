from moonleap.utils.quote import quote
from titan.widgetspec.styles import get_style_groups


def sort_styles(styles):
    # Sort styles by order of appearance in style_order.
    # Wildcards are matched using fnmatch.
    # We return a list of strings, such that styles that belong to the same group
    # are placed in the same string.

    result = []
    unused_styles = list(styles)
    has_prop_classname = False

    for group in get_style_groups():

        quoted_group_styles = []
        unquoted_group_styles = []

        for style in list(unused_styles):
            if style == "props.className":
                has_prop_classname = True
                continue

            for style_pattern in group:
                if style_pattern.is_scss:
                    continue

                if style_pattern.match(style):
                    if style_pattern.is_quoted:
                        quoted_group_styles.append(style)
                    else:
                        unquoted_group_styles.append(style)
                    unused_styles.remove(style)
                    break

        if quoted_group_styles:
            result += [" ".join(quoted_group_styles)]

        if unquoted_group_styles:
            result += [", ".join(unquoted_group_styles)]

    if has_prop_classname:
        result += ["props.className"]

    return result


def maybe_quote_style(style):
    if style.startswith("{"):
        return style

    for group in get_style_groups():
        for pattern in group:
            if not pattern.is_quoted and pattern.match(style):
                return style
    return quote(style)
