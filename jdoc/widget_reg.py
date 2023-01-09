from jdoc.scenario import *


@dataclass
class WidgetSpec(Entity):
    module_name: str
    component_term: str


class WidgetReg(Entity):
    widget_specs: list[WidgetSpec] = field(default_factory=list)

    def load_widget_specs(self):
        self.widget_specs.extend(
            [
                WidgetSpec(module_name="todos", component_term="todo:view"),
            ]
        )


global_widget_reg = WidgetReg()
