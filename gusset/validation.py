from functools import wraps
from inspect import getargspec
from fabric.api import abort


class Required(object):
    pass


def with_validation(func):
    """
    Decorator that validates task arguments:
     -  Checks the argspec for the input function
     -  Validates that all arguments have been specified with non-None values
     -  Aborts with helpful errors

    A few caveats:

    1. This decorator *MUST* be the inner most decorator because other decorators
       will typically replace the declared args with *args and **kwargs.

    2. The decorated function must use kwargs-style values with defaults of None
       instead of arg-style values. Otherwise, Fabric will raise a barely useful
       TypeError if the argumennt was not provided. That is, use:

           def foo(bar=Required):
               pass

       Instead of:

           def foo(bar):
               pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        argspec = getargspec(func)
        for index, arg_name in enumerate(argspec.args):
            arg_value = args[index] if index < len(args) else kwargs.get(arg_name)
            if arg_value is not None:
                continue
            if len(argspec.defaults) > index and argspec.defaults[index] is not Required:
                continue
            abort("Missing required argument: {}".format(arg_name))
        return func(*args, **kwargs)
    return wrapper
