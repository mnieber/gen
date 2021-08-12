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

        for content in (lhs_content, rhs_content):
            for line in content.split(os.linesep):
                if line == "export {};":
                    continue
                if line.startswith("import"):
                    if line not in header:
                        header.append(line)
                else:
                    footer.append(line)

        if header and footer:
            header.append(os.linesep)

        return os.linesep.join(header) + os.linesep.join(footer)
