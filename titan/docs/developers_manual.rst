Case 1: a service can use a Makefile
====================================

Description
-----------

The Makefile resource is associated with a Service. It collects MakefileRules and outputs them in a
Makefile for managing that service.

The example
-----------

.. code-block:: python

    body = """runserver:
    \tpython manage.py runserver 0.0.0.0:8000
    """
    )

    def get_makefile_rule():
        return MakefileRule(name="runserver", text=body)

    @create("django-app")
    def create_django(term):
        django_app = DjangoApp(name="django-app")
        add(django_app, get_makefile_rule())  # [1-2]
        return django_app

Notes
-----

1. The created Makefile will have an additional rule called 'init' that is intended to call all makefile
   rules that are necessary to initialize the service.
2. The django_app resource is a `Tool` that is associated with a `Service`. All `MakefileRule` resources associated
   with a `Tool` will automatically be used for the Makefile of that `Service`.