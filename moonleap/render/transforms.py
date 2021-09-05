_transforms = []
_post_transforms = []


def register_transforms(arg_transforms, arg_post_transforms):
    global _transforms, _post_transforms
    _transforms.extend(arg_transforms)
    _post_transforms.extend(arg_post_transforms)


def get_transforms():
    return _transforms


def get_post_transforms():
    return _post_transforms
