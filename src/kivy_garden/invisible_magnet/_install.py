from functools import partial, cache

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.factory import Factory


_installed = set()


@cache
def get_kv_filename(key):
    return f"kivy_garden.invisible_magnet.{key}"


def install(*, target='Widget', speed=10.0, animate_size=False):
    from ._main import _impl

    if isinstance(target, str):
        target_name = target
        target_cls = Factory.get(target)
    else:
        target_name = target.__name__
        target_cls = target

    if target_name in _installed:
        return
    _installed.add(target_name)

    widgets = []
    trigger = Clock.create_trigger(partial(batch_magnetize, widgets, *_impl[not animate_size], speed))
    target_cls._magnetize_soon = partial(magnetize_soon, widgets, trigger)

    Builder.load_string(
        f"<{target_name}>:\n    on_kv_post: self._magnetize_soon(self)",
        filename=get_kv_filename(target_name),
    )


def uninstall(*, target='Widget'):
    if isinstance(target, str):
        target_name = target
        target_cls = Factory.get(target)
    else:
        target_name = target.__name__
        target_cls = target

    if target_name not in _installed:
        return
    _installed.remove(target_name)
    del target_cls._magnetize_soon
    Builder.unload_file(get_kv_filename(target_name))


def uninstall_all():
    for target_name in _installed.copy():
        uninstall(target=target_name)


def magnetize_soon(widgets, trigger, widget):
    widgets.append(widget.__self__)
    trigger()


def batch_magnetize(widgets, magnetize, unmagnetize, speed, dt):
    from ._main import is_magnetized
    for w in widgets:
        if not is_magnetized(w):
            magnetize(w, speed=speed)
            w._unmagnetize = unmagnetize
    widgets.clear()
