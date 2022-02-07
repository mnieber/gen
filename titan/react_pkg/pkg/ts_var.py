from moonleap.utils.case import l0, u0
from moonleap.utils.inflect import plural
from titan.api_pkg.item.resources import Item
from titan.api_pkg.itemlist.resources import ItemList
from titan.api_pkg.itemtype.resources import ItemType


def ts_var(x):
    from titan.react_state_pkg.state import State

    if isinstance(x, Item):
        return x.item_name
    if isinstance(x, ItemList):
        return plural(x.item_name)
    if isinstance(x, State):
        return l0(x.name)
    raise Exception(f"tsvar: unknown {x}")


def ts_type_from_item_name(x):
    return f"{u0(x)}T"


def ts_form_type(x):
    if isinstance(x, Item):
        return ts_form_type_from_item_name(x.item_name)
    elif isinstance(x, ItemType):
        return ts_form_type_from_item_name(x.name)
    raise Exception(f"ts_form_type: unknown {x}")


def ts_var_by_id_type(x):
    if isinstance(x, Item):
        return ts_var_by_id_type_from_item_name(x.item_name)
    raise Exception(f"ts_form_type: unknown {x}")


def ts_form_type_from_item_name(x):
    return f"{u0(x)}FormT"


def ts_var_by_id_type_from_item_name(x):
    return f"{u0(x)}ByIdT"


def ts_var_by_id(x):
    if isinstance(x, Item):
        return ts_var(x) + "ById"
    raise Exception(f"ts_var_by_id: unknown {x}")
