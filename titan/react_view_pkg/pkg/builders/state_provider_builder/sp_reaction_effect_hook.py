from moonleap.utils import chop0

sp_reaction_effect_hook_tpl = chop0(
    """
{% magic_with state.name as MyState %}
{% magic_with named_item_list.typ.item_name as myListItem %}
{% magic_with named_item.typ.item_name as myItem %}
{% magic_with container.name as myContainer %}
    useUpdateStateReaction({
      getInputs: () => {
        return {
          {{ container_input.typ.ts_var }}: {{ __.get_data_path(container_input) }},                          {% !! container_input in __.container_inputs(containers) %}
        }
      },
      updateState: (inputs) => {
        R.forEach(initRS, inputs.myListItems ?? []);                                                          {% for container in containers %}{% for named_item_list in __.container_inputs([container], named_items=False) %}
        state.myContainer.data.myListItems = inputs.myListItems ?? [];
        {{ "" }}                                                                                              {% endfor %}
        state.myContainer.data.myItem = inputs.myItem;                                                        {% !! named_item in __.container_inputs([container], named_item_lists=False) %}{% endfor %}
        if (flags.logStateProviders) {
          log('MyState updated', state.getSummary());
        }
      },
      destroyState: () => state.destroy(),
    });
    {{ "" }}
{% end_magic_with %}
{% end_magic_with %}
{% end_magic_with %}
{% end_magic_with %}    """
)
