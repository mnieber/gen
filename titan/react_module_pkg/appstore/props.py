from titan.react_pkg.pkg.ml_get import ml_react_app


def substores(app_store):
    stores = []
    for module in ml_react_app(app_store).modules:
        if module == app_store.module:
            continue
        stores.extend(module.stores)
    return stores
