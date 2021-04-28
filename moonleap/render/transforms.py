from moonleap.render.process_magic_with import process_magic_with
from moonleap.render.process_remove_duplicate_lines import (
    post_process_remove_duplicate_lines,
    process_remove_duplicate_lines,
)
from moonleap.render.process_trim_newlines import (
    post_process_trim_newlines,
    process_trim_newlines,
)

transforms = [process_magic_with, process_remove_duplicate_lines, process_trim_newlines]
post_transforms = [post_process_remove_duplicate_lines, post_process_trim_newlines]
