import os
from pathlib import Path

from moonleap.render.merge import FileMerger


class IndexFileMerger(FileMerger):
    def matches(self, fn):
        return Path(fn).name in ["index.ts", "index.tsx", "index.js", "index.jsx"]

    def merge(self, lhs_content, rhs_content):
        header = []
        footer = []

        for content in (lhs_content, rhs_content):
            for line in content.split(os.linesep):
                if not line:
                    continue
                if line.startswith("import"):
                    if line not in header:
                        header.append(line)
                else:
                    footer.append(line)

        return os.linesep.join(header) + os.linesep.join(footer)
