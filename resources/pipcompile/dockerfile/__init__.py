def update(resource, term, line, block):
    pip_install_in_dockerfile(block, "pip-tools", ["dockerfile_dev", "dockerfile"])
