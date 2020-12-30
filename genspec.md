# Spec of the cashcog:project

The cashcog:project has a :src-dir that stores files from the mnieber/test:git-repository.
The root:layer has a server:layer-group with a stack:layer, frontend:layer and backend:layer.

## The stack:layer

The root directory has a :docker-compose and a :docker-compose-dev file.

## The frontend:layer

The frontend:service has a node_14:dockerfile and a :dockerfile-dev.
:It uses the default:root-dir and default:src-mount-point.

## The backend:layer

The backend:service has a python_3.8:dockerfile and a :dockerfile-dev.
:It uses the default:root-dir and default:src-mount-point.
:It also has a :makefile for running :pip-compile.
:It uses :pytest with :pytest-html.
