import glob, inspect, os

modules = glob.glob(os.path.dirname(__file__) + "/*.py")
__all__ = [os.path.basename(f)[:-3] for f in modules
           if not os.path.basename(f).startswith('_') and not
           f.endswith('__init__.py') and os.path.isfile(f)]


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


def get_calling_frame():
    
    frame = inspect.currentframe()
    callstack = inspect.getouterframes(frame, 2)
    caller = callstack[2][0]

    return caller


def get_current():

    frame = inspect.currentframe()
    callstack = inspect.getouterframes(frame, 1)
    frame = callstack[1][0]
    frameinfo = inspect.getframeinfo(frame)
    
    if 'self' in frame.f_locals:
        current_class = frame.f_locals['self'].__class__.__name__
    else:
        current_class = None
    
    current_module = inspect.getmodule(frame).__name__
    current_name = frameinfo[2]
    
    if current_class:
        current_string = "%s.%s" % (current_class, current_name)
    else:
        current_string = "%s" % (current_name)

    if current_module:
        current_string = "%s." % (current_module) + current_string

    return current_string


def get_current_frame():
    
    frame = inspect.currentframe()
    callstack = inspect.getouterframes(frame, 1)
    caller = callstack[1][0]

    return caller
