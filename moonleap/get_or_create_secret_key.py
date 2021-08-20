import os
import uuid

import yaml


def get_or_create_secret_key(session, key_name):
    secret_keys_fn = os.path.join(session.spec_dir, "secret_keys.yml")
    secret_keys = {}
    if os.path.exists(secret_keys_fn):
        secret_keys = yaml.load(open(secret_keys_fn))
    secret_key = secret_keys.get(key_name)
    if secret_key is None:
        secret_key = secret_keys[key_name] = str(uuid.uuid4())
        with open(secret_keys_fn, "w") as f:
            yaml.dump(secret_keys, f)
    return secret_key
