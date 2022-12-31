import os

import yaml
from titan.react_view_pkg.pkg.get_builders import get_builders

from .widget_spec_parser import WidgetSpecParser


def load_widget_specs(widget_reg, spec_dir):
    spec_dir = os.path.join(spec_dir, "ui")
    if os.path.exists(spec_dir):
        for module_spec_fn in os.listdir(spec_dir):
            fn = os.path.join(spec_dir, module_spec_fn)

            module_name = os.path.splitext(module_spec_fn)[0]
            with open(fn) as f:
                widget_spec_dict = yaml.load(f, Loader=yaml.SafeLoader)
                parser = WidgetSpecParser(
                    widget_spec_dict, module_name, get_builders, widget_reg
                )
                parser.parse(widget_spec_dict)
                try:
                    pass
                except Exception as e:
                    raise Exception(f"Error parsing {fn}: {e}")

            if False:
                widget_reg.pprint()