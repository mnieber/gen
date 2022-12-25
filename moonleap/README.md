# Moonleap

The Moonleap code generator is started via its `entrypoint`.
When Moonleap is started, the following happens:

- a `session` is created.
- the Moonleap `packages` are loaded, based on the `settings file`.
- the `spec file` is converted into a list of `blocks`.
- `resources` are created in each block.
- these `resources` are `rendered` into source files.
- the created source files are `post-processed`.
- a `report` is created that allows you to inspect the run.
