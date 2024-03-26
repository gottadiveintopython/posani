from dataclasses import dataclass
from functools import partial
from kivy.metrics import dp
from kivy.clock import Clock, ClockEvent
from kivy.uix.widget import Widget
from kivy.graphics import Translate


@dataclass(slots=True)
class Context:
    last_x: int | float
    last_y: int | float
    mat: Translate
    inv_mat: Translate
    trigger_anim_pos: ClockEvent = None


def magnetize(w: Widget, *, speed=10.0, pos_threshold=dp(2)):
    w.canvas.before.insert(0, mat := Translate())
    w.canvas.after.add(inv_mat := Translate())
    ctx = Context(w.x, w.y, mat, inv_mat)
    # NOTE: circular reference!!
    ctx.trigger_anim_pos = Clock.create_trigger(
        partial(_anim_pos, ctx, speed, -pos_threshold, pos_threshold), 0, True)
    w.bind(x=_on_x, y=_on_y)
    w._magnet_ctx = ctx


def unmagnetize(w: Widget):
    w.unbind(x=_on_x, y=_on_y)
    ctx = w._magnet_ctx
    w.canvas.before.remove(ctx.mat)
    w.canvas.after.remove(ctx.inv_mat)
    ctx.trigger_anim_pos.cancel()
    # NOTE: break the circular reference
    del ctx.trigger_anim_pos
    del w._magnet_ctx


def _on_x(w, x):
    ctx: Context = w._magnet_ctx
    mat = ctx.mat
    mat.x = dx = ctx.last_x - x + mat.x
    ctx.inv_mat.x = -dx
    ctx.last_x = x
    ctx.trigger_anim_pos()


def _on_y(w, y):
    ctx: Context = w._magnet_ctx
    mat = ctx.mat
    mat.y = dy = ctx.last_y - y + mat.y
    ctx.inv_mat.y = -dy
    ctx.last_y = y
    ctx.trigger_anim_pos()


def _anim_pos(ctx: Context, speed, threshold_min, threshold_max, dt):
    mat = ctx.mat
    inv_mat = ctx.inv_mat
    p = 1.0 - dt * speed
    still_going = False

    if p <= 0.0:
        inv_mat.x = inv_mat.y = mat.x = mat.y = 0.
        return False

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
