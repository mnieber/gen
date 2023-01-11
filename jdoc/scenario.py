import typing as T
import uuid

from dataclassy import dataclass, factory


def label(types):
    parts = [t.__class__.__name__ for t in types]
    return " ".join(parts)


@dataclass(kw_only=True)
class Scenario:
    facts: T.List[str] = []
    level: int = 0

    def add_fact(self, fact: T.Any):
        self.facts.append(self.level * " " + label(fact))
        return ScenarioContext(self)

    def add_info(self, info: str):
        pass

    def push(self):
        self.level += 1

    def pop(self):
        self.level -= 1

    # Return ScenarioContext
    def sub(self):
        return ScenarioContext(self)


# A ContextManager that calls push() and pop() on a Scenario
class ScenarioContext:
    def __init__(self, scenario: Scenario):
        self.scenario = scenario

    def __enter__(self):
        self.scenario.push()

    def __exit__(self, *args):
        self.scenario.pop()


@dataclass(kw_only=True)
class Entity:
    id: str = factory(lambda: uuid.uuid4().hex)
    _traces: T.List[str] = []

    def add_trace(self, trace: str):
        self._traces.append(trace)

    @property
    def t(self):
        return self.__class__.__name__


@dataclass(kw_only=True)
class Fn:
    name: str


def _get(f: tuple, t: T.Type[Entity]):
    for x in f:
        if isinstance(x, t):
            return x
    raise Exception(f"Could not find {t} in {f}")


def get(f: tuple, t):
    return T.cast(t, _get(f, t))


def add_traces(label, traces):
    suffix = f" ({label})"
    for (entity, trace) in traces:
        entity.add_trace(trace + suffix)


def _(x):
    return x
