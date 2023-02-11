import os
from pathlib import Path

from moonleap.render.file_merger import FileMerger


class JsFileMerger(FileMerger):
    patterns = ["index.ts", "index.tsx", "index.js", "index.jsx"]

    @classmethod
    def add_patterns(cls, patterns):
        for pattern in patterns:
            if pattern not in cls.patterns:
                cls.patterns.append(pattern)

    def matches(self, fn):
        return Path(fn).name in JsFileMerger.patterns

    def merge(self, lhs_content, rhs_content):
        header = []
        footer = []
        has_footer_content = False

        for content in (lhs_content, rhs_content):
            lines = content.split(os.linesep) if content else []
            line_idx = 0
            while line_idx < len(lines):
                line = lines[line_idx]
                line_idx += 1

                if line == "export {};":
                    continue
                elif line.startswith("import"):
                    while ";" not in line and line_idx < len(lines):
                        line += lines[line_idx]
                        line_idx += 1
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
