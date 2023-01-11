# Render react components

## Components are assigned to react-modules

When the front-end uses a :react-app, then this triggers the assign_components_to_react_modules() rule. This rule loops over the
:widget-specs, determines the corresponding component terms and creates forward:relations that link them to the different :react-modules.

## A component has pipelines

`Pipeline source`

The pipeline.source function returns pipeline's root resource, which can be some :item
or :item~list that comes from pipeline.component.props, or a :query, or a :state~provider.

`Pipeline data_path`

The pipeline.data_path function creates an expression that starts at the pipeline's source and navigates
to the given 'obj' resource. This expression can be used to get 'obj' from the
component props, or from one of the queries that the component instantiates.

## Fn build() builds a widget_spec

`The build() function`

The build() function instantiates a set of builders, one for each widget base type
in widget_spec.widget_base_types (usually, just one). Each builder creates a
:builder-output instance. The :builder-output instance are combined into a single
instance, that contains various types of content (e.g. imports, React hooks, React
elements) that are pasted into the View.tsx.j2 template.

`The Builder object`

A Builder is instantiated with a widget-spec, which is used as the source of
information for creating its :builder-output. It recursively calls build() on all
child widget specs of its widget-spec, and merges the corresponding :builder-output
instances into its own :builder-output instance.

## The ComponentBuilder

The ComponentBuilder creates React code that instantiates some React component.
