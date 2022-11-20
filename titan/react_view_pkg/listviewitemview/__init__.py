from pathlib import Path

from moonleap import create, kebab_to_camel
from moonleap.utils.case import u0

from .resources import ListViewItemView

base_tags = {"lvi-view": ["component"]}


@create("lvi-view")
def create_lvi_view(term):
    name = kebab_to_camel(term.data)
    lvi_view = ListViewItemView(item_name=name, name=f"{u0(name)}ListView")
    lvi_view.template_dir = Path(__file__).parent / "templates"
    return lvi_view
