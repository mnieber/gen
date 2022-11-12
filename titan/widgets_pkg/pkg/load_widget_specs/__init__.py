import os

import yaml

from .widget_spec_parser import WidgetSpecParser


def load_widget_specs(widget_reg, spec_dir):
    fn = os.path.join(spec_dir, "ui.yaml")
    if os.path.exists(fn):
        with open(fn) as f:
            widget_spec_dict = yaml.load(f, Loader=yaml.SafeLoader)
            parser = WidgetSpecParser(widget_reg)
            parser.parse(widget_spec_dict)
            widget_reg.pprint()
