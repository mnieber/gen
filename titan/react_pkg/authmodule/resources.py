from dataclasses import dataclass

from titan.react_pkg.reactmodule import ReactModule


@dataclass
class AuthModule(ReactModule):
    uses_username = True
