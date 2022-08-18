from titan.project_pkg.service import Tool
from dataclasses import dataclass


@dataclass
class Vandelay(Tool):
    language: str
