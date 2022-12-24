from titan.react_pkg.component.props import get_pipeline_and_data_path


def get_data_path(widget_spec, obj):
    ws = widget_spec
    while ws:
        # Search first in the component
        if component := ws.component:
            data_path = component.get_data_path(obj=obj)
            if data_path:
                return data_path

        # Search in the pipelines for this widget_spec
        pipeline, data_path = get_pipeline_and_data_path(ws.pipelines, obj=obj)
        if data_path:
            return data_path
        ws = ws.parent_ws
    return None
