from moonleap.render.process_magicwith import process_magicwith
from moonleap.render.process_trim_newlines import (
    post_process_trim_newlines,
    process_trim_newlines,
)

transforms = [process_magicwith, process_trim_newlines]
post_transforms = [post_process_trim_newlines]
