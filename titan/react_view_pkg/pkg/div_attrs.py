def update_div_attrs(div_attrs, prefix_classes=None, handlers=None, key=None):
    div_attrs = div_attrs or {}
    result = dict(div_attrs)
    if prefix_classes:
        result["classes"] = prefix_classes + div_attrs.get("classes", [])
    if handlers:
        result["handlers"] = div_attrs.get("handlers", []) + handlers
    if key:
        result["key"] = key
    return result
