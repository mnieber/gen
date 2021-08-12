from moonleap import rule, tags
from titan.project_pkg.service import create_service

keycloak_env_fn = "./env/keycloak.env"


@tags(["keycloak:service"])
def create_keycloak(term, block):
    keycloak_service = create_service(term, block)
    keycloak_service.env_files.append(keycloak_env_fn)
    return keycloak_service


@rule("keycloak:service")
def keycloak_service_created(keycloak_service):
    keycloak_service.port = keycloak_service.port or "8080"
    keycloak_service.project.add_template_dir(__file__, "templates")
