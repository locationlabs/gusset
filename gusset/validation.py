from functools import wraps
from inspect import getargspec
from fabric.api import abort


class Required(object):
    """
    Marker class for required arguments.
    """
    pass


def with_validation(func):
    """
    Decorator that validates task arguments:
     -  Checks the argspec for the input function
     -  Validates that all arguments have been specified with non-None values
     -  Aborts with helpful errors

    One caveat: this decorator *MUST* be the innermost decorator because other
    decorators will typically replace the declared args with *args and **kwargs.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        assert_valid_arguments(func, *args, **kwargs)
        return func(*args, **kwargs)
    return wrapper


def assert_valid_arguments(func, *args, **kwargs):
    """
    Validate provided arguments against a function's argspec.
    """
    # get the function argspec
    argspec = getargspec(func)

    func_defaults = argspec.defaults or tuple()
    defaults = (Required,) * (len(argspec.args) - len(func_defaults)) + func_defaults
    for index, arg_name in enumerate(argspec.args):
        arg_value = args[index] if index < len(args) else kwargs.get(arg_name)
        if arg_value is not None:
            continue
        if defaults[index] is not Required:
            continue
        abort("Missing required argument: {}".format(arg_name))
