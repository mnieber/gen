from moonleap.parser.term import match_term_to_pattern


def get_data_path(widget_spec, term):
    ws = widget_spec
    while ws:
        component = ws.component
        if component:
            pipeline, data_path = component.get_pipeline_and_data_path(term=term)
            if data_path:
                return data_path

        # HACK: use widget_base_type to determine data path
        if ws.widget_base_type in ("Array", "ListView"):
            from titan.react_view_pkg.pkg.get_builder import get_builder

            b = get_builder(ws)
            if term and match_term_to_pattern(b.named_item_list_term, term):
                return term.data

        ws = ws.parent
    return None
