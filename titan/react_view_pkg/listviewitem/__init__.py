from pathlib import Path

from moonleap import create, kebab_to_camel
from moonleap.utils.case import u0

from .resources import ListViewItem

base_tags = {"lvi": ["component"]}


@create("lvi")
def create_lvi_view(term):
    name = kebab_to_camel(term.data)
    lvi = ListViewItem(item_name=name, name=f"{u0(name)}ListViewItem")
    lvi.template_dir = Path(__file__).parent / "templates"
    return lvi
