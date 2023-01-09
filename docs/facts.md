# :Widget-specs

## The :widget-spec-parser converts ui/ui.<module-name>.yaml into :widget-specs.

All :widget-specs are loaded when the :widget-reg is created.

## A :widget-spec can be used to instantiate a widget inside a parent widget

## A :widget-spec can be used to define a widget in its own react module

## Every component-def:widget-spec is stored in the :widget-reg.

# Components

## The `react_modules_have_components` function creates :components from :widget-specs

## The component.load_pipelines creates the pipelines for that component

Each pipeline is based on `component.widget_spec`.

A :mutation has a run:method that /takes :scalars and :forms.
A form-:view stores a :mutation or a editing:behavior.
A form-:view has a :constructor that takes a mutation-name+:string or a editing-bvr+:string

- If the :constructor takes a mutation-name+:string then it has a :mutation
  -- (it can look up the mutation in the :api-reg)
- If the :constructor takes a editing-bvr+:string, then it has a editing:behavior
  -- (it can look up the editing:behavior in the :default-props of the root:component).
  A editing:behaviour has a :mutation.

Add a julia function for each fact, e.g. fact(::Scenario, ::FormView, ::MayHave, ::Mutation)

- when this function is executed, it adds data to the scenario
- the function can invoke other facts (thus adding to the scenario)
  -- in that case, we can clone the scenario if there are forks
  -- a cloned scenario can have a pointer to its parent scenario (no need to copy everything)
