# :Widget-specs

## The :widget-spec-parser converts ui/ui.<module-name>.yaml into :widget-specs.

All :widget-specs are loaded when the :widget-reg is created.

## A :widget-spec can be used to instantiate a widget inside a parent widget

## A :widget-spec can be used to define a widget in its own react module

## Every component-def:widget-spec is stored in the :widget-reg.

# Components

## The `react_modules_provide_widgets` function creates :components from :widget-specs

## The component.load_pipelines creates the pipelines for that component

Each pipeline is based on `component.widget_spec`.
