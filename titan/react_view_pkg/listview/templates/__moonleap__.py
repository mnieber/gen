import ramda as R

view_div = """
      <div
        className={cn(
          'MyItemListView', 'flex flex-col',
          props.className
        )}
      >
        {myItemDivs.length > 0 && myItemDivs}
        {myItemDivs.length === 0 && noItems}
      </div>
"""


def get_helpers(_):
    def _find_behavior(name):
        return R.find(lambda x: x.name == name)(_.component.bvrs)

    class Helpers:
        widget_spec = _.component.widget_spec
        item_name = _.component.item.item_name
        selection_bvr = _find_behavior("selection")
        deletion_bvr = _find_behavior("deletion")
        highlight_bvr = _find_behavior("highlight")
        drag_and_drop_bvr = _find_behavior("dragAndDrop")
        div = view_div.replace("MyItemListView", _.component.name).replace(
            "myItemDivs", item_name + "Divs"
        )
        components = [_.component.lvi]
        css_classes = []
        has_children = False
        has_default_props = True

        has_selection = selection_bvr
        has_highlight = selection_bvr or highlight_bvr
        has_drag_and_drop = drag_and_drop_bvr

    return Helpers()
