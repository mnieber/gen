from .transform import post_process_clean_up_js_imports, process_clean_up_js_imports

transforms = [
    process_clean_up_js_imports,
]

post_transforms = [
    post_process_clean_up_js_imports,
]
