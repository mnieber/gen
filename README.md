# Moonleap code generator

Moonleap is a tool that automates part of the work that a programmer does. Programmers are able to read
a project specification and turn it into a set of source files. Based on the words that are
used in the project description, they are able to:

1. imagine the structure of the project
2. determine tools and software that needs to be installed
3. create a minimal configuration for these tools
4. progressively fill in more details to make the system work as suggested

To what extent would a computer program be able to do this automatically? The proposition of Moonleap is
that - by using a clever and pragmatic approach - a useful skeleton project can be created from a specification
automatically. The key ideas behind this approach are:

- the spec is written in natural language, but the author helps the code generator by prefixing each noun with a
  colon and each verb with a slash, e.g. "the :project /has a backend:service". This makes for highly readable
  specs that are also easy to process programmatically.

- the code generator turns these nouns and verbs into a directed graph of resources. For every resource, code is generated
  by rendering text templates that have access to the information in that resource.

- the result is treated as a skeleton example project. This skeleton serves as the starting point for the real project.
  Changes in the skeleton can be copied to the real project using a diff/merge tool such as Meld. This way, the spec, the
  skeleton and the real project evolve side by side.

- Moonleap is intended to be customized. A developer can introduce their own set of nouns and vers, and add rules and
  templates that turn these into first resources and then source code.

## A short example

To explain how this works, consider this spec

```
## The backend:service

The backend:service uses a python_3.8:dockerfile. :It uses :pytest.
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

Moonleap turns the spec into a set of source files as follows:

1. Each term is converted into one or more resources, e.g. backend:service -> Service("backend"),
   python_3.8:dockerfile -> Dockerfile("python_3.8") and pytest -> Pytest() and PipDependency("pytest").

2. :It is an alias that resolves to the first term in the preceeding sentence. In the example that
   would be "backend:service".

3. Resources are rendered into artifacts.
