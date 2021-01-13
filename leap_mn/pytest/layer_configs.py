def get_pytest_options(pytest):
    result = dict(capture=False)

    if pytest.service and pytest.service.src_dir:
        result["src_dir"] = pytest.service.src_dir.location

    return dict(PYTEST=result)
