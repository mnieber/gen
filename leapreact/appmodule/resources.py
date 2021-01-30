from dataclasses import dataclass

from leapreact.module import Module
from moonleap import Resource


@dataclass
class AppModule(Module):
    pass


@dataclass
class CssImport(Resource):
    paths: [str]
