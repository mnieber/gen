# Spec of the cashcog:project

The cashcog:project has a :src-dir that stores files from the mnieber/test:git-repository.
The root:layer has a server:layer-group with a stack:layer, frontend:layer and backend:layer.
There is no:foobar configuration.

# Components

## Stack:layer

The root directory has a :docker-compose and a :docker-compose-dev file.

## Frontend:layer

The frontend:service has a node_14:docker-file and a :docker-file-dev.
:It uses the default:root-dir and default:src-mount-point.

## Backend:layer

The backend:service has a python_3.8:docker-file and a :docker-file-dev.
:It uses the default:root-dir and default:src-mount-point.
:It also has a :makefile for running :pip-compile.
:It uses :pytest with :pytest-html.
