from jdoc.scenario import Scenario


class RenderReactComponentsScenario(Scenario):
    pass


s = RenderReactComponentsScenario()


def add_fact(x):
    return s.add_fact(x)


def add_info(x):
    return s.add_info(x)
