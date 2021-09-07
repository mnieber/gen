import typing as T
from dataclasses import dataclass

from moonleap.parser.term import word_to_term
from moonleap.resource.rel import Rel
from moonleap.verbs import is_created_as


def is_created_as_rel(term):
    return Rel(term, is_created_as, term)


@dataclass
class Rule:
    rel: Rel
    f: T.Callable
    priority: int = 1


def rule(subj_term, verb=None, obj_term=None, priority=10):
    if verb is None or obj_term is None:
        if verb is not None or obj_term is not None:
            raise Exception("Either define both verb and obj_term or neither")
        verb = is_created_as
        obj_term = subj_term

    def wrapped(f):
        rel = Rel(
            subj=word_to_term(subj_term, default_to_tag=True),
            verb=verb,
            obj=word_to_term(obj_term, default_to_tag=True),
        )
        f.moonleap_rule = Rule(rel, f, priority=priority)
        return f

    return wrapped


def create(term_str, base_tags=None):
    def wrapped(f):
        term = word_to_term(term_str, default_to_tag=True)
        f.moonleap_create_rule_term = term, base_tags or []

        return f

    return wrapped


_add_function_by_resource_type = {}


def add(resource, child_resource):
    f = _add_function_by_resource_type.get(child_resource.__class__)
    if not f:
        raise Exception(f"No add rule is registered for {child_resource.__class__}")
    f(resource, child_resource)


def register_add(resource_type):
    def wrapped(f):
        _add_function_by_resource_type[resource_type] = f
        return f

    return wrapped


def extend(resource_type):
    def wrapped(props):
        setattr(props, "moonleap_extends_resource_type", resource_type)
        return props

    return wrapped
