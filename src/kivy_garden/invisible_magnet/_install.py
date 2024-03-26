from functools import partial
from textwrap import dedent

from kivy.clock import Clock
from kivy.lang import Builder


_installed = False


def install(*, speed=10.0, animate_size=False):
    from ._main import _impl
    global _installed
    if _installed:
        return
    _installed = True


    widgets = []
    trigger = Clock.create_trigger(partial(batch_magnetize, widgets, _impl[not animate_size][0], speed))

    global magnetize_soon
    magnetize_soon = partial(magnetize_soon, widgets, trigger)

    Builder.load_string(dedent(f'''
        #:import magnetize_soon {__name__}.magnetize_soon
        <Widget>:
            on_kv_post: magnetize_soon(self)
        '''))



def magnetize_soon(widgets, trigger, widget):
    widgets.append(widget.__self__)
    trigger()


def batch_magnetize(widgets, magnetize, speed, dt):
    from ._main import is_magnetized
    for w in widgets:
        if not is_magnetized(w):
            magnetize(w, speed=speed)
    widgets.clear()
