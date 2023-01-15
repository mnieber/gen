from .transform import post_process_min_lines, process_min_lines

transforms = [
    process_min_lines,
]

post_transforms = [post_process_min_lines]
