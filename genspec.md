# Spec of the cashcog:project

## The cashcog:project and its :dodo-config

The cashcog:project /has a :dodo-config.
:It /has a server:layer-group /with a stack:layer, frontend:layer and backend:layer.
:It /has a :src-dir that /stores files from the mnieber/test:git-repository.
:It /runs a frontend:service and a backend:service.

### The stack:layer

The stack:layer /has a :docker-compose and a :docker-compose-dev file that are used
to /run the frontend:service and backend:service.

### The frontend:service in the frontend:layer

The frontend:service /has a node_14:dockerfile and a node_14:dockerfile-dev.
:It /uses the default:root-dir and default:src-mount-point.
:It /runs :create-react-app.

### The backend:service in the backend:layer

The backend:service /has a python_3.8:dockerfile and a python_3.8:dockerfile-dev.
:It /uses the default:root-dir and default:src-mount-point.
:It also /has a :makefile for /running :pip-compile.
:It /uses :pytest /with :pytest-html.
