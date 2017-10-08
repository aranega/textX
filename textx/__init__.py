__version__ = "1.6.dev"

__PYECORE_SUPPORT = False


def is_pyecore_enabled():
    return __PYECORE_SUPPORT


def enable_pyecore_support(enable=True):
    global __PYECORE_SUPPORT
    __PYECORE_SUPPORT = enable
    import sys
    if sys.version > '3':
        try:
            from importlib import reload
        except ImportError:
            from imp import reload

    import textx.model
    import textx.metamodel
    import textx.textx
    reload(textx.metamodel)
    reload(textx.model)
    reload(textx.textx)
