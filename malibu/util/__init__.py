import glob, inspect, os

modules = glob.glob(os.path.dirname(__file__) + "/*.py")
__all__ = [os.path.basename(f)[:-3] for f in modules if not os.path.basename(f).startswith('_') and not f.endswith('__init__.py') and os.path.isfile(f)]


def get_caller():

    frame = inspect.currentframe()
    callstack = inspect.getouterframes(frame, 2)
    caller = callstack[2][0]
    callerinfo = inspect.getframeinfo(caller)
    
    if 'self' in caller.f_locals:
        caller_class = caller.f_locals['self'].__class__.__name__
    else:
        caller_class = None
    
    caller_module = inspect.getmodule(caller).__name__
    caller_name = callerinfo[2]
    
    if caller_class:
        caller_string = "%s.%s" % (caller_class, caller_name)
    else:
        caller_string = "%s" % (caller_name)

    if caller_module:
        caller_string = "%s." % (caller_module) + caller_string

    return caller_string
