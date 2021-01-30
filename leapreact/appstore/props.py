def substores(app_store):
    submodules = app_store.module.submodules.merged
    return [x.store for x in submodules]
