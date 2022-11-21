import os


def indent(level):
    tab = " " * level

    def indent_content(content):
        lines = content.split(os.linesep)
        return os.linesep.join([tab + x for x in lines])

    return indent_content
