from .transform import post_process_trim_newlines, process_trim_newlines

transforms = [
    process_trim_newlines,
]
post_transforms = [
    post_process_trim_newlines,
]
