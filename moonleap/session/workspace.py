import os
from pathlib import Path

from moonleap.packages.scope_manager import ScopeManager
from moonleap.render.file_writer import FileWriter
from moonleap.session import get_session


class Workspace:
    def __init__(self, spec_dir, output_root_dir):
        self.spec_dir = spec_dir
        self.output_root_dir = output_root_dir
        self.output_dir = f"{output_root_dir}/output"
        self.expected_dir = f"{output_root_dir}/expected"
        self.snapshot_fn = f"{output_root_dir}/snapshot.json"
        self.type_specs_dir = os.path.join(self.spec_dir, "type_specs")
        self.scope_manager = None
        self.file_writer = None

    def init(self, is_smart):
        self.scope_manager = ScopeManager()
        self.file_writer = FileWriter(
            self.snapshot_fn,
            check_crc_before_write=is_smart,
            root_dir=self.output_dir,
        )
        packages_by_scope = get_session().settings.get("packages_by_scope", {})
        self.scope_manager.import_packages(packages_by_scope)

    @property
    def spec_fn(self):
        spec_fn = Path(self.spec_dir) / "spec.md"
        if not spec_fn.exists():
            raise Exception(f"Spec file not found: {spec_fn}")
        return spec_fn
