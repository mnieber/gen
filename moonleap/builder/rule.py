import typing as T
from dataclasses import dataclass

from moonleap.parser.term import word_to_term
from moonleap.resource.rel import Rel
from moonleap.verbs import is_created_as


@dataclass
class Rule:
    rel: Rel
    f: T.Callable
    fltr_subj: T.Callable = None
    fltr_obj: T.Callable = None
    description: str = None


def rule(subj_term, verb, obj_term, fltr_subj=None, fltr_obj=None, description=None):
    def wrapped(f):
        rel = Rel(
            subj=word_to_term(subj_term, default_to_tag=True),
            verb=verb,
            obj=word_to_term(obj_term, default_to_tag=True),
        )
        f.moonleap_rule = Rule(
            rel, f, fltr_subj=fltr_subj, fltr_obj=fltr_obj, description=description
        )
        return f

    return wrapped


def created(subj_term):
    return rule(subj_term, is_created_as, subj_term)


def tags(tags):
    def wrapped(f):
        f.moonleap_create_rule_by_tag = {}
        for tag in tags:
            f.moonleap_create_rule_by_tag[tag] = f

        return f

    return wrapped


_add_function_by_resource_type = {}


def add(resource, child_resource):
    f = _add_function_by_resource_type.get(child_resource.__class__)
    if not f:
        raise Exception(f"No add rule is registered for {child_resource._class__}")
    f(resource, child_resource)


def register_add(resource_type):
    def wrapped(f):
        _add_function_by_resource_type[resource_type] = f
        return f

    return wrapped


def describe(description):
    def wrapped(f):
        f.moonleap_description = description
        return f

    return wrapped


def extend(resource_type):
    def wrapped(props):
        setattr(props, "moonleap_extends_resource_type", resource_type)
        return props

    return wrapped
