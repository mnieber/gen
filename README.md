# Moonleap code generator

Moonleap is a tool that automates part of the work that a programmer does. Programmers are able to read
a project specification and turn it into a set of source files. Based on the words that are
used in the project description, they are able to:

1. imagine the structure of the project
2. determine tools and software that need to be installed
3. create a minimal configuration for these tools
4. progressively fill in more details to make the system work as suggested

To what extent would a computer program be able to do this automatically? The proposition of Moonleap is
that - by using a clever and pragmatic approach - a useful skeleton project can be created from a specification
automatically. The key ideas behind this approach are:

- the spec is written in natural language, where the author helps the code generator by prefixing each noun with a
  colon and each verb with a slash, e.g. "the :project /has a backend:service". This makes for highly readable
  specs that are also easy to process programmatically.

- the code generator turns these nouns and verbs into a directed graph of resources. For every resource, code is generated
  by rendering text templates that have access to the information in that resource.

- the result is treated as a skeleton example project that serves as the starting point for the real project.
  Changes in the skeleton can be copied to the real project using a diff/merge tool such as Meld. This way, the spec, the
  skeleton and the real project evolve side by side. More importantly, it means that the skeleton project does not have to be
  perfect, it only has to be useful.

- Moonleap is intended to be customized. A developer can introduce their own set of nouns and verbs, and add rules and
  templates that turn these into first resources and then source code.

## Running

```
pip install requirements.txt
python gen.py specs/titan.md
ls output  # or better: tree output
```

## A short example

To explain how this works, consider this spec

```
## The backend:service

The backend:service /uses a python_3.8:dockerimage. :It /uses :pytest.
```

A developer can add a rule for turning "backend:service" into a resource:

```
@dataclass
class Service:
    name: str

@tags(["service"])
def create_service(term, block):
    return Service(name=term.data)
```

The developer can then configure the set of the templates that take this resource as input:

```
@extend(Service)
class ExtendService:
    render = MemFun(render_templates(__file__), "templates")
```

Moonleap turns the spec into a set of source files as follows:

1. Each term is converted into one or more resources, e.g. for backend:service we create`Service("backend")`,
   for python_3.8:dockerimage we create `DockerImage("python_3.8")` and for :pytest we create a `Pytest()` resource
   that points to a `PipDependency("pytest")` resource.

2. :It is an alias that resolves to the first term in the preceeding sentence. In the example that
   would be "backend:service".

3. Resources are rendered into artifacts. The rendering process uses the graph-structure that connects all
   the resources. In our example we can set up the rendering rules such that the pytest pip package is installed inside the Dockerfile
   (based on the `PipDependency("pytest")` and `Dockerfile("python_3.8")` resources in the graph).
