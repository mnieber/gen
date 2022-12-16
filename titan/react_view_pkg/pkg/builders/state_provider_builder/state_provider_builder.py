from moonleap import Tpls, append_uniq, chop0
from titan.react_view_pkg.pkg.builder import Builder

from .sp_preamble import return_value, sp_preamble_tpl
from .sp_reaction_effect_hook import sp_reaction_effect_hook_tpl
from .sp_state_hook import delete_items_data, order_items_data, sp_state_hook_tpl


class StateProviderBuilder(Builder):
    def build(self):
        self.output.has_children = True
        self.output.no_scss = True

        state_provider = self.widget_spec.component
        state = state_provider.state
        containers = state.containers if state else []
        pipelines = state_provider.pipelines

        queries, mutations = [], []
        _get_endpoints_from_pipelines(pipelines, queries, mutations)
        _get_mutations_from_containers(containers, mutations)

        functions = dict(
            delete_items_data=delete_items_data,
            order_items_data=order_items_data,
            container_inputs=_container_inputs,
            return_value=lambda data, hint=None: return_value(
                state_provider, containers, data, hint
            ),
            get_data_path=state_provider.get_data_path,
        )

        context = dict(
            containers=containers,
            mutations=mutations,
            queries=queries,
            state=state,
            state_provider=state_provider,
            more_type_specs_to_import=_more_type_specs_to_import(mutations),
            __=functions,
        )

        self.add(
            imports=[tpls.render("sp_imports_tpl", context)],
            preamble_hooks=[
                tpls.render("sp_preamble_hooks_tpl", context),
                tpls.render("sp_state_hook_tpl", context),
                tpls.render("sp_reaction_effect_hook_tpl", context),
            ],
            preamble=[tpls.render("sp_preamble_tpl", context)],
            lines=[tpls.render("sp_return_value_tpl", context)],
        )


def _get_endpoints_from_pipelines(pipelines, queries, mutations):
    for pipeline in pipelines:
        pipeline_source = pipeline.source
        if pipeline_source.meta.term.tag == "query":
            append_uniq(queries, pipeline_source)
        if pipeline_source.meta.term.tag == "mutation":
            append_uniq(mutations, pipeline_source)


def _get_mutations_from_containers(containers, mutations):
    for container in containers:
        if delete_items_mutation := container.delete_items_mutation:
            append_uniq(mutations, delete_items_mutation)
        if delete_item_mutation := container.delete_item_mutation:
            append_uniq(mutations, delete_item_mutation)
        if order_items_mutation := container.order_items_mutation:
            append_uniq(mutations, order_items_mutation)


def _container_inputs(containers, named_items=True, named_item_lists=True):
    result = []
    for container in containers:
        if named_items:
            for named_item in container.named_items:
                result.append(named_item)
        if named_item_lists:
            if container.named_item_list:
                result.append(container.named_item_list)
    return result


def _more_type_specs_to_import(mutations):
    types = []
    for mutation in mutations:
        for field in mutation.api_spec.get_inputs(
            ["fk", "relatedSet", "uuid", "uuid[]"]
        ):
            append_uniq(types, field.target_type_spec)
    return types


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

tpls = Tpls(
    "state_provider_builder",
    sp_imports_tpl=sp_imports_tpl,
    sp_preamble_tpl=sp_preamble_tpl,
    sp_preamble_hooks_tpl=sp_preamble_hooks_tpl,
    sp_state_hook_tpl=sp_state_hook_tpl,
    sp_reaction_effect_hook_tpl=sp_reaction_effect_hook_tpl,
    sp_return_value_tpl=sp_return_value_tpl,
)
