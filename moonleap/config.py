import typing as T
from dataclasses import dataclass
from pathlib import Path

from moonleap.parser.term import fuzzy_match, word_to_term
from moonleap.rel import Rel


class Config:
    def __init__(self):
        self.create_rule_by_term = {}
        self.derive_rules_by_resource_type = {}
        self.meta_by_resource_type = {}
        self.rules = []

    def get_create_rule(self, subject_term):
        result = None
        for term, rule in config.create_rule_by_term.items():
            if subject_term.tag == term.tag:
                if term.data:
                    if subject_term.data == term.data:
                        return rule
                elif not result:
                    result = rule
        return result

    def get_derive_rules(self, resource_type):
        return self.derive_rules_by_resource_type.get(resource_type) or {}

    def get_rules(self, input_rel, subj_resource, obj_resource):
        return [
            rule
            for rule in self.rules
            if fuzzy_match(input_rel, rule.rel)
            and (not rule.fltr_subj or rule.fltr_subj(subj_resource))
            and (not rule.fltr_obj or rule.fltr_obj(obj_resource))
        ]

    def add_rule(self, rule):
        self.rules.append(rule)

    def get_meta(self, resource_type):
        return self.meta_by_resource_type.get(resource_type, {})

    def get_templates(self, resource):
        templates = self.get_meta(resource.__class__).get("templates", lambda x: "")
        return templates(resource)

    def get_output_dir(self, resource):
        output_dir = self.get_meta(resource.__class__).get("output_dir", "")
        return output_dir(resource) if callable(output_dir) else output_dir


config = Config()


def derive(resource_type):
    def wrapped(f):
        f.moonleap_derive_resource = resource_type
        return f

    return wrapped


@dataclass
class Rule:
    rel: Rel
    f: T.Callable
    fltr_subj: T.Callable = None
    fltr_obj: T.Callable = None
    description: str = None


def rule(
    subject_term, verb, object_term, fltr_subj=None, fltr_obj=None, description=None
):
    def wrapped(f):
        rel = Rel(
            subj=word_to_term(subject_term, default_to_tag=True),
            verb=verb,
            obj=word_to_term(object_term, default_to_tag=True),
        )
        f.moonleap_rule = Rule(
            rel, f, fltr_subj=fltr_subj, fltr_obj=fltr_obj, description=description
        )
        return f

    return wrapped


def tags(tags):
    def wrapped(f):
        f.moonleap_create_rule_by_tag = {}
        for tag in tags:
            f.moonleap_create_rule_by_tag[tag] = f

        return f

    return wrapped


def output_dir_from(prop_name):
    def get_output_dir(resource):
        if hasattr(resource, prop_name):
            prop = getattr(resource, prop_name)
            return config.get_output_dir(prop)
        return ""

    return get_output_dir


def output_path_from(prop_name):
    return lambda x: Path(output_dir_from(prop_name)(x))


def extend(resource_type):
    def wrapped(props):
        setattr(props, "moonleap_extends_resource_type", resource_type)
        return props

    return wrapped
