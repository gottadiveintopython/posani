from dataclasses import dataclass
from functools import partial
from kivy.metrics import dp
from kivy.clock import Clock, ClockEvent
from kivy.uix.widget import Widget
from kivy.graphics import Translate, Scale, PushMatrix, PopMatrix, InstructionGroup


@dataclass(slots=True)
class Context:
    last_x: int | float
    last_y: int | float
    last_width: int | float
    last_height: int | float
    translate: Translate
    scale: Scale
    pop_mat: PopMatrix
    ig: InstructionGroup
    trigger_anim_pos: ClockEvent = None
    trigger_anim_size: ClockEvent = None


def magnetize(w: Widget, *, speed=10.0, pos_threshold=dp(2), scale_threshold=0.005):
    w.canvas.before.insert(0, ig := InstructionGroup())
    w.canvas.after.add(pop_mat := PopMatrix())
    ig.add(PushMatrix())
    ig.add(translate := Translate())
    ig.add(scale := Scale(origin=w.pos))
    ctx = Context(w.x, w.y, w.width, w.height, translate, scale, pop_mat, ig)
    # NOTE: circular references!!
    ctx.trigger_anim_pos = Clock.create_trigger(
        partial(_anim_pos, ctx, speed, -pos_threshold, pos_threshold), 0, True)
    ctx.trigger_anim_size = Clock.create_trigger(
        partial(_anim_size, ctx, speed, -scale_threshold + 1.0, scale_threshold + 1.0), 0, True)
    w.bind(x=_on_x, y=_on_y, width=_on_width, height=_on_height)
    w._magnet_ctx = ctx


def unmagnetize(w: Widget):
    w.unbind(x=_on_x, y=_on_y, width=_on_width, height=_on_height)
    ctx = w._magnet_ctx
    w.canvas.before.remove(ctx.ig)
    w.canvas.after.remove(ctx.pop_mat)
    ctx.trigger_anim_pos.cancel()
    ctx.trigger_anim_size.cancel()
    # NOTE: break the circular references
    del ctx.trigger_anim_pos
    del ctx.trigger_anim_size
    del w._magnet_ctx


def _on_x(w, x):
    ctx = w._magnet_ctx
    t = ctx.translate
    t.x = ctx.last_x - x + t.x
    ctx.last_x = x
    ctx.scale.origin = (x, ctx.last_y)
    ctx.trigger_anim_pos()


def _on_y(w, y):
    ctx = w._magnet_ctx
    t = ctx.translate
    t.y = ctx.last_y - y + t.y
    ctx.last_y = y
    ctx.scale.origin = (ctx.last_x, y)
    ctx.trigger_anim_pos()


def _on_width(w, width):
    ctx = w._magnet_ctx
    ctx.scale.x *= ctx.last_width / width
    ctx.last_width = width
    ctx.trigger_anim_size()


def _on_height(w, height):
    ctx = w._magnet_ctx
    ctx.scale.y *= ctx.last_height / height
    ctx.last_height = height
    ctx.trigger_anim_size()


def _anim_pos(ctx: Context, speed, threshold_min, threshold_max, dt):
    t = ctx.translate
    p = 1.0 - dt * speed
    still_going = False

    if p <= 0.0:
        t.x = t.y = 0.
        return False

    if threshold_min < (x := t.x) < threshold_max:
        t.x = 0.
    else:
        t.x = x * p
        still_going = True

    if threshold_min < (y := t.y) < threshold_max:
        t.y = 0.
    else:
        t.y = y * p
        still_going = True

    return still_going


def _anim_size(ctx: Context, speed, threshold_min, threshold_max, dt):
    s = ctx.scale
    p = 1.0 - dt * speed
    still_going = False

    if p <= 0.0:
        s.x = s.y = 1.
        return False

    if threshold_min < (sx := s.x) < threshold_max:
        s.x = 1.
    else:
        s.x = (sx - 1.0) * p + 1.0
        still_going = True

    if threshold_min < (sy := s.y) < threshold_max:
        s.y = 1.
    else:
        s.y = (sy - 1.0) * p + 1.0
        still_going = True

    return still_going
