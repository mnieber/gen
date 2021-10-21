from pathlib import Path

import ramda as R
from moonleap.resource.prop import Prop

from .resources import OutputPath


def output_path():
    def get(self):
        elements = self.output_paths.elements
        return None if not elements else elements[0].location

    def set(self, output_path):
        elements = self.output_paths.elements
        if len(elements) > 0:
            raise Exception(f"Output path was already set")

        child = OutputPath(output_path)
        elements.append(child)

    return Prop(get_value=get, set_value=set)


def merged_output_path():
    def _merge(acc, x):
        return OutputPath(location=(x.location + acc.location))

    def get_value(resource):
        return Path(
            R.reduce(_merge, OutputPath(""), resource.output_paths.merged).location
        )

    return Prop(get_value=get_value)
