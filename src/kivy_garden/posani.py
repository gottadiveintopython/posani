__all__ = (
    'activate', 'deactivate', 'is_active',
    'install', 'uninstall', 'uninstall_all',
)
from math import exp as math_exp
from dataclasses import dataclass
from functools import partial

from kivy.metrics import dp
from kivy.clock import Clock, ClockEvent
from kivy.uix.widget import Widget
from kivy.graphics import Translate
from kivy.lang import Builder


#------------------------------------------------------------------------------------------
# Core
#------------------------------------------------------------------------------------------


@dataclass(slots=True)
class Context:
    last_x: int | float
    last_y: int | float
    mat: Translate
    inv_mat: Translate
    trigger_anim_pos: ClockEvent = None


def is_active(w: Widget) -> bool:
    return hasattr(w, '_posani_ctx')


def activate(w: Widget, *, speed=10.0, min_diff=dp(2)):
    '''
    :param speed: The speed coefficient for the animation. A larger value results in faster animation.
    :param min_diff: When the difference between the widget's real and displayed positions is less than this value,
                     the displayed position will instantly snap to the real one. Defaults to 2dp.
    '''
    if is_active(w):
        return
    w.canvas.before.insert(0, mat := Translate())
    w.canvas.after.add(inv_mat := Translate())
    ctx = Context(w.x, w.y, mat, inv_mat)
    ctx.trigger_anim_pos = Clock.create_trigger(
        partial(_anim_pos, math_exp, mat, inv_mat, -speed, -min_diff, min_diff), 0, True)
    w.bind(x=_on_x, y=_on_y)
    w._posani_ctx = ctx


def deactivate(w: Widget):
    if not is_active(w):
        return
    w.unbind(x=_on_x, y=_on_y)
    ctx = w._posani_ctx
    w.canvas.before.remove(ctx.mat)
    w.canvas.after.remove(ctx.inv_mat)
    ctx.trigger_anim_pos.cancel()
    del w._posani_ctx


def _on_x(w, x):
    ctx: Context = w._posani_ctx
    mat = ctx.mat
    mat.x = diff = ctx.last_x - x + mat.x
    ctx.inv_mat.x = -diff
    ctx.last_x = x
    ctx.trigger_anim_pos()


def _on_y(w, y):
    ctx: Context = w._posani_ctx
    mat = ctx.mat
    mat.y = diff = ctx.last_y - y + mat.y
    ctx.inv_mat.y = -diff
    ctx.last_y = y
    ctx.trigger_anim_pos()


def _anim_pos(math_exp, mat, inv_mat, neg_speed, min, max, dt):
    p = math_exp(neg_speed * dt)
    still_going = False

    if min < (x := mat.x) < max:
        x = inv_x = 0.
    else:
        x *= p
        inv_x = -x
        still_going = True

    if min < (y := mat.y) < max:
        y = inv_y = 0.
    else:
        y *= p
        inv_y = -y
        still_going = True

    mat.xy = x, y
    inv_mat.xy = inv_x, inv_y
    return still_going


#------------------------------------------------------------------------------------------
# Installation
#------------------------------------------------------------------------------------------

_installed = set()


def _kv_filename(key):
    return f"kivy_garden.posani.{key}"


INST_STR = '''
#:import posani_activate kivy_garden.posani.activate
<{}>:
    on_kv_post: posani_activate(self)
'''


def install(*, target='Widget'):
    if target in _installed:
        return
    _installed.add(target)
    Builder.load_string(INST_STR.format(target), filename=_kv_filename(target))


def uninstall(*, target='Widget'):
    if target not in _installed:
        return
    _installed.remove(target)
    Builder.unload_file(_kv_filename(target))


def uninstall_all():
    for target in _installed.copy():
        uninstall(target=target)
