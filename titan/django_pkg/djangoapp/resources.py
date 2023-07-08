import typing as T
from dataclasses import dataclass, field

from moonleap import Resource, get_session
from moonleap.utils.get_or_create_secret_key import get_or_create_secret_key
from titan.project_pkg.service import Tool


@dataclass
class DjangoApp(Tool):
    translation_ids: T.List[str] = field(default_factory=list)

    @property
    def secret_key_dev(self):
        return get_or_create_secret_key(get_session(), "django_dev")

    def __post_init__(self):
        pass

    @property
    def use_translation(self):
        return False

    @property
    def add_tests(self):
        return False

    def add_translation(self, id, value, translations):
        if id in self.translation_ids:
            return
        self.translation_ids.append(id)
        translations.append((id, value))


@dataclass
class DjangoAdminReorder(Resource):
    pass


@dataclass
class DjangoDbBackup(Resource):
    pass
