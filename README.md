# Gusset

Small utilities for Fabric scripts.

[![Build Status](https://travis-ci.org/locationlabs/gusset.png)](https://travis-ci.org/locationlabs/gusset)

## Output Control

Fabric supports flexible output control, though integrating Fabric's output
with the output of your scripts isn't as easy as it should be.

Here's how Gusset helps:

 1. Provides `status` and `debug` functions that respect Fabrics output controls
    and use the same message format that Fabric uses internally:
 
        from fabric.api import settings
        from gusset.output import debug, status
        
        with settings(host_string="localhost"):
            debug("Debug message")
            status("Status message")            

 2. Provides a simple way to control output levels with a single `verbosity`
    parameter:
    
        from gusset.output import configure_output
        
        configure_output(verbosity=1)

 3. Provides the `with_output` decorator for fabric tasks:
 
        from fabric.api import task
        from gusset.output import with_output
        
        @task
        @with_output(verbosity=1)
        def my_task():
            pass

## Validation

Fabric's command line argument parsing is very powerful, but it provides unusable
`TypeErrors` if a required argument is omitted.

Here's how Gusset helps:

 1. Provides the `Required` marker value as the default for required parameters so that
    Fabric's command line won't balk if they are not provided:
    
        from fabric.api import task
        from gusset.validation import Required
        
        @task
        def my_task(myarg=Required):
            pass
 
 2. Provides the `with_validation` decorator to enforce that all required parameters
    have values, generating a useful error otherwise:

        from fabric.api import task
        from gusset.validation import Required, with_validation
        
        @task
        @with_validation
        def my_task(myarg=Required):
            pass

Note that the `with_validation` decorator currently must be the innermost decorator of
your task function.
