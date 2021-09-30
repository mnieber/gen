Purpose
=======

The react_pkg allows you to add a react app to the stack.
Below, the process will be explained using annotated use-cases.

Case 1: a router is added to the stack
======================================

Description
-----------

The router is declared in the spec by stating that "the react:app /has a :router".
To add a route you should declare in the spec that a react module shows a component, e.g.
"the todos:module /shows the dashboard:view". These components are called "root components".
The router resource will find and include all root components in all react modules,
taking the following points into consideration:

1. If a root component wraps other components (e.g. "the dashboard:view /wraps a todo:list-view")
then the wrapped components are also added to the route. If a component has more than 1 wrapped
component then this creates branches in the router tree.

2. Each component provides so-called router configs through a "get_router_configs" member function.
As will be explained below, these router configs provide url parts from which the urls in the router
are constructed. They may also provide additional parent components (such as React context providers)
that the component must be wrapped in.

3. If `get_router_configs` returns more than 1 router config, then the last router config corresponds
to the component itself (`C`) and the former router configs correspond to parent components that C is
wrapped in. In other words, the router configs indicate a nested component structure, e.g. `X(Y(C))`.
Every router config has a `url` field that adds a url part. For example, if `X` contributes
"/todos" and `Y` contributes "/todo/:todoId" and `C` contributes "/todo-view" then the complete url associated
with `C` is `/todos/todo/:todoId/todo-view`.

The first step in constructing the router component is to collect all the routes, using the following steps:

1. For every root component C, we add `C.get_router_configs()` as a preliminary route. We say that C is the
terminal component of this route. The route is preliminary because if C wraps other components, then these
component will extend the route.
2. If the terminal component of a route does not wrap any other component, then we add this route to the list
of final routes.
3. Otherwise, we enter a recursion, where the call `get_router_configs` on the wrapped route, and append the
result to the preliminary route. This yields a new route that has a terminal component thay may or may not
wrap additional components (hence the recursion).

The seconds step is to construct the router component from these routes, using these steps:

1. We initialize the tree level to 0 and the url to ""
2. All routes are grouped by their first router config. Every group is a new branch in the router tree.
3. For every group, we check if first router config in that group has a url. If so, we add a corresponding
Route component to the router. Then, we add the component (for that same router config) to the router. We
take into account whether the component wraps child components, or not. In the first case, we only add the
React tag that starts the component (which means that later we have to close that tag).
4. Now we recurse, using (tree level + 1), the new url value, and the routes within the current group.
5. If needed, we close the React tag that was opened in step 3.

Note that the final nesting structure depends on how components are wrapped into other components.
For any component C, there are two ways in which this wrapping can be specified:
a) the spec may specify that some component C* wraps C, or b) the call to `C.get_router_configs()` may return
a router config that states that C* wraps C. Regardless of how the wrapping was specified, the router will try
to create a common parent route when two components share a part of their url.



