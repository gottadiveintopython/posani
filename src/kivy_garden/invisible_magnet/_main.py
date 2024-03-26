def immediate_call(f):
    return f()


@immediate_call
def _impl():
    from . import _pos_and_size as pas
    from . import _pos_only as po
    return(
        (pas.magnetize, pas.unmagnetize, ),
        (po.magnetize, po.unmagnetize, ),
    )


def is_magnetized(widget) -> bool:
    return hasattr(widget, '_unmagnetize')


def magnetize(widget, *, speed=10.0, animate_size=False):
    widget = widget.__self__
    if is_magnetized(widget):
        raise ValueError('Already magnetized')
    if speed <= 0.0:
        raise ValueError('Speed must be greater than zero')
    magnetize, unmagnetize = _impl[not animate_size]
    magnetize(widget, speed=speed)
    widget._unmagnetize = unmagnetize


def unmagnetize(widget):
    widget = widget.__self__
    if not is_magnetized(widget):
        raise ValueError('Not magnetized')
    widget._unmagnetize(widget)
    del widget._unmagnetize
