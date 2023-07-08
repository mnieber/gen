from pathlib import Path

from moonleap import get_tpl
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder


class FormStateProviderBuilder(Builder):
    type = "FormStateProvider"

    def __post_init__(self):
        self.tpl = None

    def build(self):
        self.add_div_open()
        self.add_body()
        self.add_div_close()

    def add_div_open(self):
        context = self.get_context()
        self.tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        self.output.add(lines=[self.tpl.get_section("div_open")])

    def add_div_close(self):
        assert self.tpl
        self.output.add(lines=[self.tpl.get_section("div_close")])

    def add_body(self):
        assert self.tpl
        add_tpl_to_builder(self.tpl, self)

    def get_context(self):
        return dict()
