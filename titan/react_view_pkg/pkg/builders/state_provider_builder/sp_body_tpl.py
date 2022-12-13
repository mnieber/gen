from moonleap.utils import chop0

sp_imports_tpl = chop0(
    """
{% magic_with query.name as myQuery %}
{% magic_with mutation.name as myMutation %}
{% magic_with state.name as MyState %}
import { observer } from 'mobx-react-lite';
import * as R from 'ramda';
import React from 'react';
import { NestedDefaultPropsContext } from 'react-default-props-context';
import { maybe, initRS, setToUpdating } from 'src/api/ResourceState';
import { MyState } from 'src/{{ state.state_provider.module.module_path }}/MyState';            {% ?? state %}
import { {{ type_spec.type_name }}T } from 'src/api/types/{{ type_spec.type_name }}T';          {% !! type_spec in more_type_specs_to_import %}
import { useMyQuery } from 'src/api/queries';                                                   {% !! query in queries %}
import { useMyMutation } from 'src/api/mutations';                                              {% !! mutation in mutations %}
import { defaultProps as dps, withDefaultProps } from 'src/app/defaultProps';
import { flags } from 'src/app/flags';
import { useUpdateStateReaction } from 'src/frames/hooks/useUpdateStateReaction';
import { lookUp, getIds } from 'src/utils/ids';
import { log } from 'src/utils/logging';
{% end_magic_with %}
{% end_magic_with %}
{% end_magic_with %}
    """
)

sp_preamble_hooks_tpl = chop0(
    """
{% magic_with query.name as myQuery %}
{% magic_with mutation.name as myMutation %}
    const myQuery = useMyQuery();                                                               {% !! query in queries %}
    const myMutation = useMyMutation();                                                         {% !! mutation in mutations %}
{% end_magic_with %}
{% end_magic_with %}
    """
)


sp_return_value_tpl = chop0(
    """
      <NestedDefaultPropsContext value={getDefaultPropsContext()}>
        {props.children}
      </NestedDefaultPropsContext>
"""
)
