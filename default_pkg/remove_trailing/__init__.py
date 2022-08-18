from .transform import post_process_remove_trailing, process_remove_trailing

transforms = [
    process_remove_trailing,
]

post_transforms = [post_process_remove_trailing]
