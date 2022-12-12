from moonleap.parser.term import match_term_to_pattern
from titan.react_view_pkg.pkg.get_named_data_term import get_named_item_list_term


def get_data_path(widget_spec, term):
    ws = widget_spec
    while ws:
        if component := ws.component:
            data_path = component.get_data_path(term=term)
            if data_path:
                return data_path

        # HACK: use widget_base_type to determine data path
        for widget_base_type in ws.widget_base_types:
            if widget_base_type in ("Array", "ListView"):
                item_name = get_named_item_list_term(ws).data
                if term and term.data == item_name and term.tag == "item":
                    return item_name

        ws = ws.parent_ws
    return None
