from dataclasses import dataclass, field

from moonleap import Resource
from titan.project_pkg.service import Tool


@dataclass
class DjangoApp(Tool):
    pass


@dataclass
class DjangoConfig(Resource):
    settings: dict = field(default_factory=dict)
    urls: list = field(default_factory=list)
    urls_imports: list = field(default_factory=list)
    cors_urls: list = field(default_factory=list)
