import re

attr_patterns = [
    r"onClick",
]


def is_attr(part):
    for attr_pattern in attr_patterns:
        if re.fullmatch(attr_pattern, part):
            return True
    return False
