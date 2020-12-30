# Spec of the linsci:project

The :src-dir stores files from the mnieber/linsci:git-repository.
The server:layer-group has a stack:layer, frontend:layer and backend:layer.

# Components

## Stack

The root directory has a :docker-compose and a :docker-compose-dev file.

## Frontend

The frontend:service has a node_14:docker-file and a :docker-file-dev.
:It uses: the default:root-dir and default:src-mount-point.
:It uses :create-react-app with :typescript, :ant-design and :tailwindcss.
:It uses a :url-router.

### The session:module

The session:module contains a session:ctr.
The session:ctr has a [navigation:facet](facets/navigation.md).
:It also has a test:facet.

### The move-lists:module

The move-lists:module contains a move-lists:store.

## Backend

The backend:service has a python_3.8:dockerfile and a :dockerfile-dev.
:It uses the default:root-dir and default:src-mount-point.
:It also has a :makefile for running :pip-compile.
:It uses :pytest with :pytest-html.
:It uses :django and :django-graphene.
