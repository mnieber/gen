import yaml


def load_yaml(fn):
    with open(fn) as f:
        return yaml.load(f, Loader=yaml.SafeLoader)
