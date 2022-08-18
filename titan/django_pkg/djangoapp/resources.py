from dataclasses import dataclass

from moonleap import get_session
from moonleap.utils.get_or_create_secret_key import get_or_create_secret_key
from titan.project_pkg.service import Tool


@dataclass
class DjangoApp(Tool):
    def secret_key(self):
        return get_or_create_secret_key(get_session(), "django_dev")

    @property
    def use_translation(self):
        return True
