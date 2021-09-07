import os
from pathlib import Path

from moonleap.render.merge import FileMerger


class JsFileMerger(FileMerger):
    patterns = ["index.ts", "index.tsx", "index.js", "index.jsx"]

    @classmethod
    def add_pattern(cls, pattern):
        if pattern not in cls.patterns:
            cls.patterns.append(pattern)

    def matches(self, fn):
        return Path(fn).name in JsFileMerger.patterns

    def merge(self, lhs_content, rhs_content):
        header = []
        footer = []
        has_footer_content = False

        for content in (lhs_content, rhs_content):
            for line in content.split(os.linesep):
                if line == "export {};":
                    continue
                elif line.startswith("import"):
                    if line not in header:
                        header.append(line)
                else:
                    has_footer_content = has_footer_content or bool(line)
                    footer.append(line)

        if header and footer:
            header.append(os.linesep)

        if header or has_footer_content:
            return os.linesep.join(header) + os.linesep.join(footer)
        return "export {};"
