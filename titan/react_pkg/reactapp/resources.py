import typing as T
from dataclasses import dataclass, field

from moonleap.utils.fp import extend_uniq
from titan.project_pkg.service import Tool


@dataclass
class ReactApp(Tool):
    flags: T.List[str] = field(default_factory=list, init=False, repr=False)

    def set_flags(self, flags):
        extend_uniq(self.flags, flags)

    def has_flag(self, pkg_name):
        return pkg_name in self.flags
