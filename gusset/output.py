"""
Output control utilities.
"""
import warnings
from functools import wraps
from fabric.api import env
from fabric.state import output
from fabric.utils import warn


def with_output(verbosity=1):
    """
    Decorator that configures output verbosity.
    """
    def make_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            configure_output(verbosity=verbosity)
            return func(*args, **kwargs)
        return wrapper
    return make_wrapper


def _puts(message, level, **kwargs):
    """
    Generate fabric-style output if and only if status output
    has been selected.
    """
    if not output.get(level):
        return
    print "[{hostname}] {message}".format(hostname=env.host_string,
                                          message=message.format(**kwargs))


def status(message, **kwargs):
    """
    Generate fabric-style output if and only if status output
    has been selected.
    """
    _puts(message, 'status', **kwargs)


def debug(message, **kwargs):
    """
    Generate fabric-style output if and only if debug output
    has been selected.
    """
    _puts(message, 'debug', **kwargs)


def warn_via_fabric(message, category, filename, lineno=None, line=None):
    """
    Adapt Python warnings to Fabric's warning output manager.
    """
    warn(message.message)


def configure_output(verbosity=0, output_levels=None, quiet=False):
    """
    Configure verbosity level through Fabric's output managers.

    Provides a default mapping from verbosity levels to output types.

    :param verbosity: an integral verbosity level
    :param output_levels: an optional mapping from Fabric output types to verbosity
    :param quiet: specifies that all output should be suppressed

    This function is designed to work with command line argument parsing.
    For example:

        # configure argparse
        parser.add_option("-q", dest="quiet", action="store_true", default=False)
        parser.add_option("-v", dest="verbosity", action="count", default=0)

        # configure output
        configure_output(options.verbosity, options.quiet)
    """
    verbosity = verbosity if not quiet else -1

    output_levels = output_levels or {
        "status": 0,
        "aborts": 0,
        "user": 1,
        "warnings": 1,
        "running": 1,
        "stdout": 2,
        "stderr": 2,
        "debug": 2
    }

    # configure output manager levels via verbosity
    for manager, level in output_levels.iteritems():
        output[manager] = level <= verbosity

    # Hook up Python warnings to warning output manager
    warnings.showwarning = warn_via_fabric
    warnings.simplefilter("always", UserWarning)
