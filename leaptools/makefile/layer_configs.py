def get_make_options():
    return dict(
        ROOT=dict(decorators=dict(docker=["make"])),
        MAKE=dict(cwd=r"${/SERVER/src_dir}"),
    )
