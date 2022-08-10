import typing as T
from dataclasses import dataclass
from xmlrpc.client import boolean

from titan.project_pkg.service import Tool


@dataclass
class ReactApp(Tool):
    use_webvitals: boolean = False
