import re


def process_right_column(lines, template_fn=None):
    result = []

    for line in lines:
        prev_lines = []
        this_line = line
        next_lines = []
        all_lines = []

        def append_tag(tag):
            lines = next_lines if tag.startswith("{% end") else prev_lines
            lines.append(tag)
            all_lines.append(tag)

        for match in reversed(list(re.finditer(r"{%\s*[^%]+\s*%}", line))):
            l, r = match.span()
            tail = this_line[r:]
            if tail.strip():
                # not a tag in the right column
                break

            tag = this_line[l:r]

            # remove tag in the right column from this_line
            this_line = this_line[:l]

            append_tag(tag)

        has_only_tags = all_lines and not this_line.strip()
        if has_only_tags:
            result.extend(reversed(all_lines))
        else:
            result.extend(reversed(prev_lines))
            result.append(this_line.rstrip())
            result.extend(reversed(next_lines))

    return result


def post_process_right_column(lines, template_fn=None):
    return lines
