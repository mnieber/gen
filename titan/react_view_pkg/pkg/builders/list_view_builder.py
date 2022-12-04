from moonleap.utils import chop0
from titan.react_view_pkg.pkg.builder import Builder

view_div = chop0(
    """
{myItemDivs.length > 0 && myItemDivs}
{myItemDivs.length === 0 && noItems}"""
)

click_handler_div = chop0(
    """
const handleClick = new ClickToSelectItems({
    selection: props.myItemsSelection
});

"""
)

default_widget_spec = {"ListViewItem with Div[cn=__]": "pass"}

items_div = chop0(
    """
const todoDivs = props.todos.map((todo: TodoT) => {
    return (
        <TodoListViewItem
        key={todo.id}
        todo={todo}
        isSelected={todo && props.todosSelection.ids.includes(todo.id)}
        isHighlighted={todo && props.todosHighlight.id === todo.id}
        dragState={dragState(props.todosDragAndDrop.hoverPosition, todo.id)}
        onDelete={() => props.todosDeletion.delete([todo.id])}
        {...handleClick.handle(todo.id)}
        {...props.todosDragAndDrop.handle(todo.id)}
        />
    );
    })
)();

    """
class ListViewItemsBuilder(Builder):
    def build(self):
        item_name = self.item_list.item.item_name
        items_name = plural(item_name)

        div = view_div.replace("myItem", item_name)
        self.add_lines([div])

        bvrs = self.widget_spec.values.get("bvrs", [])
        if "selection" in bvrs:
            self.add_lines([click_handler_div.replace("myItems", items_name)])

        lvi_widget_spec = self.find_child_with_place("ListViewItem")
        if not lvi_widget_spec:

