# Spec of the cashcog:project

The :src-dir stores files from the mnieber/test:git-repository.
The server:layer-group has a stack:layer, frontend:layer and backend:layer.
There is no:foobar configuration.

# Components

## Stack

The root directory has a :docker-compose and a :docker-compose-dev file.

## Frontend

The frontend:service has a node_14:docker-file and a :docker-file-dev.
:It uses the default:root-dir and default:src-mount-point.

## Backend

The backend:service has a python_3.8:docker-file and a :docker-file-dev.
:It uses the default:root-dir and default:src-mount-point.
:It also has a :makefile for running :pip-compile.
:It uses :pytest with :pytest-html.
