import os
from pathlib import Path

import ramda as R
from moonleap import get_session
from moonleap.utils.case import sn


def make_abs(service, p):
    result = Path(p)
    if not Path(os.path.expandvars(p)).is_absolute():
        base_path = Path("/opt/projects") / service.project.kebab_name / service.name
        result = base_path / p
    return result


def get_helpers(_):
    class Helpers:
        add_bundle_volume = [x for x in _.project.services if x.use_create_bundle]

        def get_image(self, service):
            if service.dockerfile:
                return sn(_.project.name) + "_" + sn(service.name) + "_dev"
            return service.docker_image.name

        @property
        def pudb_path(self):
            return R.path_or("pudb", ["pudb_opt_path"])(get_session().settings)

    return Helpers()


def get_meta_data_by_fn(_, __):
    return {
        "docker-compose.dev.override.yml.j2": {
            "name": _.docker_compose.override_fn,
            "include": bool(_.docker_compose.override_fn),
        },
        "docker-compose.prod.yml.j2": {
            "include": bool(_.project.has_prod_config),
        },
    }
