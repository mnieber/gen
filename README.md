# Moonleap code generator

Moonleap is a tool that automates part of the work that a programmer does. Programmers are able to read
a loosely structured project specification and turn it into a set of source files. Based on the words that are
used in the project description, they are able to:

1. imagine the structure of the project
2. determine tools and software that needs to be installed
3. create a minimal configuration for these tools
4. progressively fill in more details to make the system work as suggested

To what extent would a computer program be able to do this automatically? It depends on what quality we expect.
To achieve high quality (something close to what a real programmer would created), we need a very
sophisticated program. But is we lower our expectations, then there is quite a lot of code that can still
be generated.

## Main ideas

The main ideas behind moonleap are the following:

1. Most projects have a similar structure, e.g. a set of services that have dockerfiles. Therefore,
   based on a loosely structured description, we can infer a lot of things that are likely to be true.
   For example, if we loosely describe a system with three services that each have a dockerfile, then just
   from the word "docker-compose" we can predict that we want a docker compose file with those services.

2. Even if the inferred "facts" are wrong, then it's useful to generate source files from such a description
   that can serve as the starting point for our project. For example, if our docker-compose file should really
   only have two of the three services, then we can use most of the generated file.

3. We can help moonleap by using tags in our loose description, e.g. the term "#dockerfile" tells moonleap that
   we are talking about the "dockerfile" resource.

4. We can also help moonleap by using tags in section headers. For example, a section called
   "The #dockerfile of the backend#service" tells moonleap that the section is used to describe details of these
   two resources.

To explain how this works, consider this spec

```
## The backend:service

The backend:service uses a python_3.8:dockerfile. :It uses :pytest.
```

Moonleap turns the spec into a set of source files as follows:

1. Each term is converted into one or more resources, e.g. backend:service -> Service("backend"),
   python_3.8:dockerfile -> Dockerfile("python_3.8") and pytest -> Pytest() and PipDependency("pytest").

2. Since :backend_service is mentioned in a section header, it is treated as a sink
   that can absorb the :dockerfile resource created inside that section.

3. :It is an alias that resolves to the first term in the preceeding sentence. In the example that
   would be "backend:service".

4. Resources are rendered into artifacts.
