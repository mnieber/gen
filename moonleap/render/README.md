# Render

Resources that must be converted into source files inherit the `render_mixin`.
The `render_mixin` adds a `renders` function that adds a `render task` to the `render cascade`.
The `render_task` calls `render_templates` one or more template directories.
The `render_templates` function calls `render_template` on every template.
The output of `render_template` is stored on disk by the `file writer`.
The `file writer` may use a `file merger` to merge several outputs together.
