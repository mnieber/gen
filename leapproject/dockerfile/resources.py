from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Dockerfile(Resource):
    is_dev: bool = False
    install_command: str = "apt-get install -y"
    image_name: str = None

    @property
    def name(self):
        return "Dockerfile" + (".dev" if self.is_dev else "")
