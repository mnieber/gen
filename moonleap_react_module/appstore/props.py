def substores(app_store):
    modules = app_store.module.service.modules.merged
    stores = []
    for x in modules:
        stores.extend(x.stores)
    return stores
