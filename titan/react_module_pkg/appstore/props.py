def substores(app_store):
    stores = []
    for module in app_store.module.react_app.modules:
        if module == app_store.module:
            continue
        stores.extend(module.stores)
    return stores
