from dataclasses import dataclass
import typing as T
from functools import partial
import itertools
import math
from kivy.metrics import dp
from kivy.properties import BooleanProperty, ListProperty
from kivy.clock import Clock, ClockEvent
from kivy.uix.widget import Widget
from kivy.graphics import Translate, Scale, PushMatrix, PopMatrix, CanvasBase


@dataclass(slots=True)
class Context:
    prev_x: int
    prev_y: int
    prev_width: int
    prev_height: int
    translate: Translate = None
    scale: Scale = None
    push_mat: PushMatrix = None
    pop_mat: PopMatrix = None
    anim_x: bool = False
    anim_y: bool = False
    anim_width: bool = False
    anim_height: bool = False
    trigger_anim: ClockEvent = None


def magnetize(w: Widget, *, pos=True, size=True):
    w = w.__self__
    scale = None
    translate = None
    if hasattr(w, '_magnet_ctx'):
        raise ValueError('Already magnetized')
    before_insert = w.canvas.before.insert
    if size:
        before_insert(0, scale := Scale(origin=w.pos))
    if pos:
        before_insert(0, translate := Translate())
    before_insert(0, push_mat := PushMatrix())
    w.canvas.after.add(pop_mat := PopMatrix())
    ctx = Context(
        w.x, w.y, w.width, w.height,
        translate, scale, push_mat, pop_mat,
    )

    w.fbind('x')



def on_x(ctx: Context, widget, x):
    translate = ctx.translate
    translate.x = ctx.prev_x - x + translate.x
    widget.canvas.before[0].xy = -x, -y
    widget.canvas.after[0].xy = x, y


def anim(abs, sqrt, ctx: Context, dt):
    translate = ctx.translate
    scale = ctx.scale
    if ctx.anim_width:
        new_scale_x = sqrt(scale.x)
        if 0.99 < new_scale_x < 1.01:
            new_scale_x = 1.0
            ctx.anim_width = False
        scale.x = new_scale_x

        scale.x = ctx.prev_width + abs * 10
    if translate
    translate.x += 10
    if translate.x > 100:
        widget.canvas.before[0].xy = 0, 0
        widget.canvas.after[0].xy = 0, 0
        ctx.trigger_anim.cancel()
        ctx.trigger_anim = None