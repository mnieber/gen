import os

import ramda as R

remove_duplicate_lines_tag = "{% remove_duplicate_lines %}"
end_remove_duplicate_lines_tag = "{% end_remove_duplicate_lines %}"


def process_remove_duplicate_lines(lines):
    def t(x):
        has_tag = x == remove_duplicate_lines_tag or x == end_remove_duplicate_lines_tag

        return ("{% raw %}" + x + "{% endraw %}" + os.linesep) if has_tag else x

    return R.map(t, lines)


def post_process_remove_duplicate_lines(lines):
    result = []
    removing = False
    known_lines = []
    count = 0

    for line in lines:
        if line == remove_duplicate_lines_tag:
            count += 1
            removing = True
            known_lines.clear()
            continue

        if line == end_remove_duplicate_lines_tag:
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
            "{% remove_duplicate_lines %} not matched equally by {% end_remove_duplicate_lines %}"
        )

    return result
