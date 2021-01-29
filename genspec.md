# The donationbox:project

The donationbox:project /has a :src-dir that /stores files from the mnieber/test:git-repository.
:It /has a frontend:service that is /configured in the frontend:layer.
:It /has a backend:service that is /configured in the backend:layer.
:It /uses a :vscode-project.

## The config:layer and stack:layer

The donationbox:project /has a config:layer that /has a service:layer-group that /contains the stack:layer, frontend:layer and backend:layer.
:It /has a :docker-compose and a dev:docker-compose file that are used
to /run the frontend:service and backend:service.
Both :docker-compose and dev:docker-compose are /configured by the stack:layer.

## The frontend:service

The frontend:service /has a :dockerfile and a dev:dockerfile that /use the node:13-alpine:docker-image.
:It /uses the default:root-dir and default:src-mount-point.
:It /uses the :fish shell.
:It /has a :node-package that /uses :create-react-app /with :tailwind-css, :prettier.
:It has an app:module that has a :router.

## The backend:service

The backend:service /has a :dockerfile and a dev:dockerfile that /use the python:3:docker-image.
:It /runs :django.
:It /has an :opt-dir and a :setup-file.
:It /uses the default:root-dir and default:src-mount-point.
:It /has a :makefile for /running :pip-compile.
:It /uses the :fish shell.
:It /uses (:pytest /with :pytest-html), :pudb and :isort.
