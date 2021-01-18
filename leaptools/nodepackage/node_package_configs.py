def get(node_package):
    return {
        "name": node_package.service.name,
        "version": "0.1.0",
        "private": True,
        "dependencies": {},
    }
