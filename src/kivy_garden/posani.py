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


def activate(w: Widget, *, speed=10.0, pos_threshold=dp(2)):
    if is_active(w):
        return
    w.canvas.before.insert(0, mat := Translate())
    w.canvas.after.add(inv_mat := Translate())
    ctx = Context(w.x, w.y, mat, inv_mat)
    # NOTE: circular reference!!
    ctx.trigger_anim_pos = Clock.create_trigger(
        partial(_anim_pos, math_exp, ctx, speed, -pos_threshold, pos_threshold), 0, True)
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
    # NOTE: break the circular reference
    del ctx.trigger_anim_pos
    del w._posani_ctx


def _on_x(w, x):
    ctx: Context = w._posani_ctx
    mat = ctx.mat
    mat.x = dx = ctx.last_x - x + mat.x
    ctx.inv_mat.x = -dx
    ctx.last_x = x
    ctx.trigger_anim_pos()


def _on_y(w, y):
    ctx: Context = w._posani_ctx
    mat = ctx.mat
    mat.y = dy = ctx.last_y - y + mat.y
    ctx.inv_mat.y = -dy
    ctx.last_y = y
    ctx.trigger_anim_pos()


def _anim_pos(math_exp, ctx: Context, speed, threshold_min, threshold_max, dt):
    mat = ctx.mat
    inv_mat = ctx.inv_mat
    p = math_exp(-speed * dt)
    still_going = False

    if threshold_min < (x := mat.x) < threshold_max:
        inv_mat.x = mat.x = 0.
    else:
        mat.x = x = x * p
        inv_mat.x = -x
        still_going = True

    if threshold_min < (y := mat.y) < threshold_max:
        inv_mat.y = mat.y = 0.
    else:
        mat.y = y = y * p
        inv_mat.y = -y
        still_going = True

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
