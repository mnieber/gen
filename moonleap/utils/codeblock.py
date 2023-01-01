import os


def i(level):
    tab = " " * 4 * level

    def indent(content):
        if not content:
            return content

        terminal = content[-1]
        if terminal == os.linesep:
            content = content[:-1]
        lines = content.split(os.linesep)
        return os.linesep.join([tab + x for x in lines]) + terminal

    return indent


def j(lines):
    return os.linesep.join(lines)


def get_indent(x):
    short_x = x.lstrip()
    return len(x) - len(short_x), short_x


class CodeBlock:
    def __init__(self, parent=None, level=0):
        self.result = ""
        self.parent = parent
        self.i = i(level)
        self.tab_size = 2

    def add(self, x):
        if self.parent:
            self.parent.add(self.i(x))
        else:
            self.result += self.i(x)

    def abc(self, head):
        indent, head = get_indent(head)
        tab = " " * indent * self.tab_size
        self.add(tab + head + os.linesep)

    def block(self, level):
        return CodeBlock(parent=self, level=level)

    def IxI(self, head, *parts):
        indent, head = get_indent(head)
        tab = " " * indent * self.tab_size

        if parts:
            args, tail = parts
            opn = "("
            cls = ")"
            result = f"{tab}{head}{opn}{', '.join(args)}{cls}{tail}{os.linesep}"

            if len(result) < 90:
                self.add(result)
            else:
                self.add(f"{tab}{head}{opn}{os.linesep}")
                for i in range(len(args)):
                    arg = args[i]
                    comma = "," if i < len(args) - 1 else ""
                    self.add(tab + "    " + arg + comma + os.linesep)
                self.add(f"{tab}{cls}{tail}{os.linesep}")

    def _x_(self, head, *parts):
        indent, head = get_indent(head)
        tab = " " * indent * self.tab_size

        if parts:
            args, tail = parts
            result = f"{tab}{head}{', '.join(args)}{tail}{os.linesep}"

            if len(result) < 90:
                self.add(result)
            else:
                self.add(f"{tab}{head}{os.linesep}")
                for arg in args:
                    self.add(tab + "    " + arg + os.linesep)
                self.add(f"{tab}{tail}{os.linesep}")


if __name__ == "__main__":
    root = CodeBlock()
    root.IxI("def hello_world", ["name"], ":")
    root.IxI("  print", ["'Hello, {}!'.format(name)"], "")
    root._x_("  if ", ["name == 'Alice'"], ":")
    b = root.block(2)
    b.IxI("print", ["'Hello, Alice!'"], "")

    print(root.result)
