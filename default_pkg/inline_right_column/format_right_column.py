import math
import re


def format_right_column(fn):
    with open(fn) as ifs:
        lines = ifs.readlines()

    line_len_cutoff = 120
    line_parts = []
    right_column_pos = 0

    for lineIdx in range(len(lines)):
        line = lines[lineIdx]
        left_part = line
        right_part = None
        for match in reversed(list(re.finditer(r"{%\s*[^%]+\s*%}", line))):
            l, r = match.span()
            if line[r:].strip():
                # we are no longer in the right column
                break

            left_part = line[:l].rstrip()
            right_part = line[l:].lstrip()

        left_part_len = len(left_part.replace("\t", "    "))
        if left_part and right_part is not None and left_part_len < line_len_cutoff:
            right_column_pos = max(right_column_pos, left_part_len)
            line_parts.append((left_part, right_part))
        else:
            if len(line) < line_len_cutoff:
                right_column_pos = max(right_column_pos, len(line))
            line_parts.append((line, None))

    result = []
    right_column_pos = (math.ceil(right_column_pos / 4) * 4) + 8
    for left_part, right_part in line_parts:
        if right_part is None:
            result.append(left_part)
        else:
            left_part_len = len(left_part.replace("\t", "    "))
            result.append(
                left_part + " " * (right_column_pos - left_part_len) + right_part
            )

    if lines != result:
        with open(fn, "w") as f:
            f.write("".join(result))


if __name__ == "__main__":
    import sys

    format_right_column(sys.argv[1])
