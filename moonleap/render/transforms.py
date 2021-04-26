from moonleap.render.process_magic_with import process_magic_with
from moonleap.render.process_remove_duplicates import (
    post_process_remove_duplicates,
    process_remove_duplicates,
)
from moonleap.render.process_trim_newlines import (
    post_process_trim_newlines,
    process_trim_newlines,
)

transforms = [process_magic_with, process_remove_duplicates, process_trim_newlines]
post_transforms = [post_process_remove_duplicates, post_process_trim_newlines]
