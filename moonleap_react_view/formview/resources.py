from dataclasses import dataclass

from moonleap.utils import title
from moonleap.utils.inflect import plural
from moonleap_react.component import Component


@dataclass
class FormView(Component):
    item_name: str
