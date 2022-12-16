import os
import re

from moonleap.render.render_template import render_template


class Tpl:
    def __init__(self, content):
        self.section_by_name = {}
        self._get_section_by_name(content)

    def _get_section_by_name(self, content):
        section = None
        section_name = None
        for line in content.splitlines():
            if match := re.search(r"{% section (\w+) %}", line):
                section = []
                section_name = match.group(1)
            elif match := re.search(r"{% end_section %}", line):
                assert section is not None
                self.section_by_name[section_name] = os.linesep.join(section)
                section = section_name = None
            elif section is not None:
                section += [line]

    def get_section(self, name):
        return self.section_by_name.get(name)


def get_tpl(fn, context):
    content = render_template(fn, context)
    return Tpl(content)
