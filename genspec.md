# Spec of the cashcog:project

The :src-dir stores files from the mnieber/test:git-repository.
The server:layer-group has a stack:layer, frontend:layer and backend:layer.
There is no:foobar configuration.

# Components

## Stack

The root directory has a :docker_compose and a :docker_compose_dev file.

## Frontend

The frontend:service has a node_14:docker_file and a :docker_file_dev.
:It uses the default:root_dir and default:src_mount_point.

## Backend

The backend:service has a python_3.8:docker_file and a :docker_file_dev.
:It uses the default:root_dir and default:src_mount_point.
:It also has a :makefile for running :pip-compile.
:It uses :pytest with :pytest_html.
