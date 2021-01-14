FROM {{ res.image_name }}

# install pkg dependencies
{% for pkg in res.service.get_pkg_dependencies() %}
RUN {{ res.install_command }} \
{% body %}
    {{ pkg + (' \\' if not loop.last else '') }}

# install pip dependencies
{% for pkg in res.service.get_pip_dependencies() %}
RUN pip install \
{% body %}
    {{ pkg + (' \\' if not loop.last else '') }}
