from jdoc.scenario import Scenario


class GenerateCodeScenario(Scenario):
    pass


s = GenerateCodeScenario()


def add_fact(x):
    return s.add_fact(x)


def add_info(x):
    return s.add_info(x)
