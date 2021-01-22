from leaptools.optdir import OptPath

pudb_opt_path = OptPath(
    is_dir=True,
    from_path="pudb",
    to_path="/root/.config/pudb",
)

ipython_opt_path = OptPath(
    is_dir=True,
    from_path="ipython",
    to_path="/root/.ipython",
)
