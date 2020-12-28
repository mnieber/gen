from leap_mn.dockerfile import pip_install_in_dockerfile


def update(block, pipcompile_term, dummy_term):
    pip_install_in_dockerfile(block, "pip-tools", ["dockerfile_dev", "dockerfile"])
