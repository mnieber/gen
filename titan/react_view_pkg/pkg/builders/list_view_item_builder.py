from moonleap import Tpls, chop0
from moonleap.utils.fp import append_uniq
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_builder_mixin import BvrsBuilderMixin
from titan.react_view_pkg.pkg.get_named_data_term import get_named_item_term


class ListViewItemBuilder(Builder, BvrsBuilderMixin):
    def __init__(self, widget_spec):
        Builder.__init__(self, widget_spec)
        BvrsBuilderMixin.__init__(self)

    def build(self):
        context = self._get_context()

        self.add(
            imports_lines=[tpls.render("lvi_imports_tpl", context)],
            props_lines=[tpls.render("lvi_props_tpl", context)],
            scss_lines=[tpls.render("lvi_scss_tpl", context)],
        )

    def update_widget_spec(self):
        context = self._get_context()

        if not get_named_item_term(self.widget_spec):
            self.widget_spec.values["item"] = f"+{self.bvrs_item_name}:item"

        if div_styles := tpls.render("lvi_div_styles_tpl", context):
            append_uniq(self.widget_spec.div.styles, div_styles)

        if div_attrs := tpls.render("lvi_div_attrs_tpl", context):
            append_uniq(self.widget_spec.div.attrs, div_attrs)

    def _get_context(self):
        return {
            **self.bvrs_context(),
            "item_name": self.bvrs_item_name,
            "component_name": self.widget_spec.widget_class_name,
            "uikit": True or self.use_uikit,
        }


lvi_imports_tpl = chop0(
    """
import {                                                                                {% if bvrs_has_drag_and_drop %}
  dragAndDropUIHandlers,
  DragAndDropUIPropsT,
} from 'skandha-facets/DragAndDrop';                                                    {% endif %}
import {                                                                                {% if bvrs_has_selection %}
  selectionUIHandlers,
  SelectionUIPropsT,
} from 'skandha-facets/Selection';                                                      {% endif %}
  """
)

lvi_fields_tpl = chop0(
    """
{% magic_with _.component.item_name as myItemName %}
{% magic_with field_spec.name as fieldSpecName %}
        <div>                                                                           {% for field_spec in fields %}{% if field_spec.display %}
          {props.myItemName.fieldSpecName}                                              {% ?? field_spec.field_type not in ("boolean",) %}
          fieldSpecName: {props.myItemName.fieldSpecName ? 'Yes' : 'No'}                {% ?? field_spec.field_type in ("boolean",) %}
        </div>                                                                          {% endif %}{% endfor %}
{% end_magic_with %}
{% end_magic_with %}
"""
)

lvi_props_tpl = chop0(
    """
isHighlighted: boolean;                                                                 {% ?? bvrs_has_selection %}
dragAndDropUIProps: DragAndDropUIPropsT;                                                {% ?? bvrs_has_drag_and_drop %}
selectionUIProps: SelectionUIPropsT;                                                    {% ?? bvrs_has_selection %}
  """
)

lvi_div_attrs_tpl = chop0(
    """
{...selectionUIHandlers(props.selectionUIProps)}                                        {% ?? bvrs_has_selection %}
{...dragAndDropUIHandlers(props.dragAndDropUIProps)}                                    {% ?? bvrs_has_drag_and_drop %}
  """
)

lvi_div_styles_tpl = chop0(
    """
{% magic_with component_name as MyComponent %}
{                                                                                       {% min_lines count=3 %}
  'MyComponent--selected': props.selectionUIProps.isSelected,                           {% ?? bvrs_has_selection %}
  'MyComponent--highlighted': props.isHighlighted,                                      {% ?? bvrs_has_highlight %}
},                                                                                      {% end_min_lines %}
`MyComponent--drag-${props.dragAndDropUIProps.dragState}`                               {% ?? bvrs_has_drag_and_drop %}
{% end_magic_with %}
  """
)

lvi_scss_tpl = chop0(
    """
{% magic_with component_name as myComponent %}
.MyComponent {
  @apply cursor-pointer;                                                {% ?? uikit %}
  cursor: pointer;                                                      {% ?? not uikit %}
}

.MyComponent--selected {                                                {% if bvrs_has_selection %}
  @apply bg-blue-200;                                                   {% ?? uikit %}
  background-color: #2222dd;                                            {% ?? not uikit %}
}                                                                       {% endif %}

.MyComponent--highlighted {                                             {% if bvrs_has_highlight %}
  @apply font-bold;                                                     {% ?? uikit %}
  font-weight: bold;                                                    {% ?? not uikit %}
}                                                                       {% endif %}

.MyComponent--drag-before {                                             {% if bvrs_has_drag_and_drop %}
  border-top: solid;
}

.MyComponent--drag-after {
  border-bottom: solid;
}                                                                       {% endif %}
{% end_magic_with %}
    """
)

tpls = Tpls(
    "list_view_item_builder",
    lvi_imports_tpl=lvi_imports_tpl,
    lvi_fields_tpl=lvi_fields_tpl,
    lvi_props_tpl=lvi_props_tpl,
    lvi_div_attrs_tpl=lvi_div_attrs_tpl,
    lvi_div_styles_tpl=lvi_div_styles_tpl,
    lvi_scss_tpl=lvi_scss_tpl,
)
