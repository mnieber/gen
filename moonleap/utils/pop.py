def pop(name, x):
    if x in name:
        name = name.replace(x, "").strip()
        return name, True
    return name, False
