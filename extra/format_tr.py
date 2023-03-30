from moonleap.utils import chop_suffix


def format_tr(fn):
    with open(fn) as ifs:
        lines = ifs.readlines()

    blocks = []
    block = None
    for line in lines:
        if not block and line.rstrip().endswith(": {"):
            block = [line]
        elif block:
            block.append(line)
            if chop_suffix(line.rstrip(), ",").endswith("}"):
                blocks.append(block)
                block = None

    blocks = sorted(blocks, key=lambda block: block[0])
    result = ["page = {\n"]
    for block in blocks:
        result.extend(block)
    result.append("}\n")

    if lines != result:
        with open(fn, "w") as f:
            f.write("".join(result))


if __name__ == "__main__":
    import sys

    format_tr(sys.argv[1])
