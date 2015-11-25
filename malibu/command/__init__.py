import glob, importlib, os
from importlib import import_module
from malibu.util.decorators import function_kw_reg

modules = glob.glob(os.path.dirname(__file__) + "/*.py")
__all__ = [os.path.basename(f)[:-3] for f in modules if not os.path.basename(f).startswith('_') and not f.endswith('__init__.py') and os.path.isfile(f)]

__command_modules = {}
command_module = function_kw_reg(__command_modules, ["name", "depends"])


def get_command_modules(package = None):

    package = __package__ if not package else package
    package_all = import_module(package)
    if not hasattr(package_all, "__all__"):
        raise AttributeError("Package %s has no __all__ attribute" % (package))

    package_all = package_all.__all__

    modules = {}
    deps = set()

    for module in package_all:
        module = import_module("{}.{}".format(package, module))
        # Just importing the code should take care of registration with the
        # decorator.

    for module, kws in __command_modules.iteritems():
        for depmod in kws["depends"]:
            deps.add(depmod)
        if kws["name"] in modules:
            # Module is already in map, don't clobber
            continue
        modules.update({kws["name"] : module})

    for module, kws in __command_modules.iteritems():
        for depmod in kws["depends"]:
            if depmod not in modules:
                modules.pop(kws["name"])

    return modules

