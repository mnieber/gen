import ramda as R

trim_newlines_marker = "<<<<<<<<<<<<TRIM NEWLINES>>>>>>>>>>>>>>>"
end_trim_newlines_marker = "<<<<<<<<<<<<END_TRIM NEWLINES>>>>>>>>>>>>>>>"


def process_trim_newlines(lines):
    def t(x):
        return (
            trim_newlines_marker
            if x == "{% trim_newlines %}"
            else end_trim_newlines_marker
            if x == "{% end_trim_newlines %}"
            else x
        )

    return R.map(t, lines)


def post_process_trim_newlines(lines):
    result = []
    trimming = False
    prev_line = None
    count = 0

    for line in lines:
        if line == trim_newlines_marker:
            count += 1
            trimming = True
            prev_line = None
            continue

        if line == end_trim_newlines_marker:
            count -= 1
            trimming = False
            prev_line = None
            continue

        if trimming and line == "" and prev_line == "":
            continue

        result.append(line)
        prev_line = line

    if count != 0:
        raise Exception(
            "{% trim_newlines %} not matched equally by {% end_trim_newlines %}"
        )

    return result
