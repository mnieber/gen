# Spec of the cashcog:project

## The cashcog:project and its :dodo-config

The cashcog:project /has a :dodo-config.
:It /has a :service-layer-group /with a stack:layer, frontend:layer and backend:layer.
:It /has a :src-dir that /stores files from the mnieber/test:git-repository.
:It /has a frontend:service and backend:service.

### The stack:layer

The cashcog:project /has a :docker-compose and a :docker-compose-dev file that are used
to /run the frontend:service and backend:service.

### The frontend:service in the frontend:layer

The frontend:service /has a :dockerfile and a :dockerfile-dev that /use the node_14:docker-image.
:It /uses the default:root-dir and default:src-mount-point.
:It /runs :create-react-app.

### The backend:service in the backend:layer

The backend:service /has a :dockerfile and a :dockerfile-dev that /use the python_3.8:docker-image.
:It /uses the default:root-dir and default:src-mount-point.
:It also /has a :makefile for /running :pip-compile.
:It /uses :pytest /with :pytest-html.
