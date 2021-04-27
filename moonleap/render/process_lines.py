import os


def process_lines(lines, remove, indent):
    def is_remove(nr):
        for block, flag in remove.items():
            if flag and block[0] <= nr <= block[1]:
                return True
        return False

    result = []
    for nr, line in lines.items():
        if not is_remove(nr):
            result.append(" " * indent + line)
    return os.linesep.join(result)
