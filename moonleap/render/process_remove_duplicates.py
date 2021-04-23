import os
import re

import ramda as R

remove_duplicates_tag = "{% remove_duplicates %}"
end_remove_duplicates_tag = "{% end_remove_duplicates %}"


def process_remove_duplicates(lines):
    def t(x):
        has_tag = x == remove_duplicates_tag or x == end_remove_duplicates_tag

        return ("{% raw %}" + x + "{% endraw %}" + os.linesep) if has_tag else x

    return R.map(t, lines)


def post_process_remove_duplicates(lines):
    result = []
    removing = False
    known_lines = []
    count = 0

    for line in lines:
        if line == remove_duplicates_tag:
            count += 1
            removing = True
            known_lines.clear()
            continue

        if line == end_remove_duplicates_tag:
            count -= 1
            removing = False
            continue

        if removing:
            if line in known_lines:
                continue
            else:
                known_lines.append(line)

        result.append(line)

    if count != 0:
        raise Exception(
            "{% remove_duplicates %} not matched equally by {% end_remove_duplicates %}"
        )

    return result
