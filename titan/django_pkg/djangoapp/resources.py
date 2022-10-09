import typing as T
from dataclasses import dataclass, field

from moonleap import get_session
from moonleap.utils.get_or_create_secret_key import get_or_create_secret_key
from titan.project_pkg.service import Tool


@dataclass
class DjangoApp(Tool):
    translation_ids: T.List[str] = field(default_factory=list)

    def secret_key(self):
        return get_or_create_secret_key(get_session(), "django_dev")

    def __post_init__(self):
        pass

    @property
    def use_translation(self):
        return True

    def add_translation(self, id, value, translations):
        if id in self.translation_ids:
            return
        self.translation_ids.append(id)
        translations.append((id, value))
