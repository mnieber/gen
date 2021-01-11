# project

- has(:dodo-config)
  --> :dodo-config.config_layer added to :project.layers
  --> :dodo-config.layer_config(ROOT) added to :project.layers[name="config"]
- has(frontend:service)
  --> :frontend:service.service added to :project.services
- has(backend_service)
  --> :backend:service.service added to :project.services
- has(:service-layer-group)
- has(:src-dir)
- has(:docker-compose)
  --> :docker-compose.layer_config(DOCKER_COMPOSE) added to :project.layers[name="config"]
- has(:docker-compose-dev)

# frontend:service

- configured_by(frontend:layer)
  --> frontend:service.layer_config(SERVER) added to frontend:layer.sections
- has(:dockerfile)
  --> install rules are forwarded to :frontend:service.dockerfile
- has(:dockerfile_dev)
  --> dev install rules are forwarded to :frontend:service.dockerfile_dev

# backend:service

- similar to frontend:service
- has(makefile)
  --> makefilerules are forwarded to backend:service.makefile

# :makefile

- runs(:pytest)
  --> :pytest resources are passed to :makefile.service

# :pytest

- with(:pytest_html)
  --> :pytest_html resources are passed to :pytest

# server-layer-group

- contains(stack:laver)
  --> stack:layer added to :server-layer-group.layers
- contains(frontend:laver)
  --> frontend:layer added to :server-layer-group.layers
- contains(backend:laver)
  --> backend:layer added to :server-layer-group.layers

# docker-compose

- runs(:docker-compose, frontend-service)
  --> frontend:service.docker_compose_config added docker-compose.sections
- runs(:docker-compose, backend-service)
  --> backend:service.docker_compose_config added docker-compose.sections

# docker-compose-dev

- runs(:docker-compose-dev, frontend-service)
  --> frontend:service.docker_compose_dev_config added to docker-compose-dev.sections
- runs(:docker-compose-dev, backend-service)
  --> backend:service.docker_compose_dev_config added to docker-compose-dev.sections

# dockerfile

- use(foo:docker-image)
  --> foo:docker-image assigned to :dockerfile.docker_image

---

What should trigger the addition of ROOT/version, etc?
