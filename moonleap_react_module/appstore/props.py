def substores(app_store):
    submodules = app_store.module.submodules.merged
    stores = []
    for x in submodules:
        stores.extend(x.stores)
    return stores
