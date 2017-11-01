__PYECORE_SUPPORT = False


def is_pyecore_enabled():
    return __PYECORE_SUPPORT


def enable_pyecore_support(enable=True):
    global __PYECORE_SUPPORT
    __PYECORE_SUPPORT = enable
    import sys
    if sys.version > '3':
        try:
            from importlib import reload as my_reload
        except ImportError:
            from imp import reload as my_reload
    else:
        my_reload = reload

    from textx import model
    from textx import metamodel
    from textx import lang
    my_reload(model)
    my_reload(metamodel)
    my_reload(lang)
