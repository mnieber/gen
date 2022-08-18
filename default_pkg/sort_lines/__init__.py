from .transform import post_process_sort_lines, process_sort_lines

transforms = [
    process_sort_lines,
]
post_transforms = [
    post_process_sort_lines,
]
