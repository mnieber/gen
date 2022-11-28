from dataclasses import dataclass
from xmlrpc.client import boolean

from titan.project_pkg.service import Tool


@dataclass
class ReactApp(Tool):
    use_web_vitals: boolean = False
    use_states: boolean = True
