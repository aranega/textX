__version__ = "1.6.dev"

__PYECORE_SUPPORT = False


def is_pyecore_enabled():
    return __PYECORE_SUPPORT


def enable_pyecore_support(enabled=True):
    global __PYECORE_SUPPORT
    __PYECORE_SUPPORT = enabled
