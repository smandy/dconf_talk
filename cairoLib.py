#!/usr/bin/env python

import math
import cairo
from math import pi

WIDTH, HEIGHT = 512, 512
RADIANS_PER_DEGREE = 2 * math.pi / 360

def text2(ctx,
         s,
         pos,
         theta = 0.0,
         face = 'Sans',
         font_size = 0.05):

    ctx.select_font_face(face)
    ctx.set_font_size(font_size) # em-square height is 90 pixels
    ctx.move_to(pos[0], pos[1]) # move to point (x, y) = (10, 90)
    ctx.show_text(s)
    ctx.stroke()

def text(ctx,
         string,
         pos,
         theta = 0.0,
         face = 'Georgia',
         font_size = 18):
    ctx.save()
    ctx.select_font_face(face , cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(font_size)
    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    x_off, y_off, tw, th = ctx.text_extents(string)[:4]
    nx = -tw/2.0
    ny = fheight/2

    ctx.translate(pos[0], pos[1])
    ctx.rotate(theta)
    ctx.translate(nx, ny)
    ctx.move_to(0,0)
    ctx.show_text(string)
    ctx.restore()


def doSquare(ctx, cx, cy, r1, r2, start, delta, fillWith = None):
    if fillWith:
        ctx.set_source_rgb (*fillWith) # Solid color
        ctx.new_path()
        ctx.arc( cx, cy , r1, start, start + delta)
        ctx.arc_negative( cx, cy , r2, start + delta, start)
        ctx.arc( cx, cy , r1, start, start + delta)
        ctx.fill()
        ctx.close_path()
    ctx.set_source_rgb (0, 0, 0) # Solid color
    ctx.new_path()
    ctx.arc( cx, cy , r1, start, start + delta)
    ctx.arc_negative( cx, cy , r2, start + delta, start)
    ctx.arc( cx, cy , r1, start, start + delta)
    ctx.stroke()
    ctx.close_path()

def doArc(ctx, cx, cy, r1, r2, start, delta, fillWith = None):
    if fillWith:
        ctx.set_source_rgb (*fillWith) # Solid color
        ctx.new_path()
        ctx.arc( cx, cy , r1, start, start + delta)
        ctx.arc_negative( cx, cy , r2, start + delta, start)
        ctx.arc( cx, cy , r1, start, start + delta)
        ctx.fill()
        ctx.close_path()
    ctx.set_source_rgb (0, 0, 0) # Solid color
    ctx.new_path()
    ctx.arc( cx, cy , r1, start, start + delta)
    ctx.arc_negative( cx, cy , r2, start + delta, start)
    ctx.arc( cx, cy , r1, start, start + delta)
    ctx.stroke()
    ctx.close_path()

    

def frange(start,stop, step=1.0):
    while start < stop:
        yield start
        start +=step

SEGMENTS = 16


fillers = { 28  : (0,   0  , 1),
            20  : (1,   0  ,   0),
}


def ringBuffer(ctx,
               pos,
               outerRadius,
               innerRadius,
               segments,
               dutyCycle,
               fillers = {}):
    dtheta = 2 * pi / segments
    wedgeTheta = dutyCycle * dtheta
    cx, cy = pos
    xs = frange(0, 2 * pi, dtheta)
    for i,x in enumerate(xs):
        print i
        fillWith = fillers.get(i, None)
        doArc( ctx, cx, cy, outerRadius, innerRadius , x, wedgeTheta, fillWith = fillWith)

def arrow(ctx, pos, theta, length,  arrowLength = None, dtheta = 15 * RADIANS_PER_DEGREE):
    if arrowLength is None:
        arrowLength = length * 0.35
    sx, sy = pos
    ex = sx + length * math.sin( theta )
    ey = sy + length * math.cos( theta )
    
    ctx.move_to (sx, sy)
    ctx.line_to (ex, ey)
    ctx.stroke()
    
    lhTheta = theta + dtheta
    ex1 = ex - arrowLength * math.sin(lhTheta)
    ey1 = ey - arrowLength * math.cos(lhTheta)
    ctx.move_to(ex1, ey1)
    ctx.line_to(ex, ey)
    ctx.stroke()

    rhTheta = theta - dtheta
    ex2 = ex - arrowLength * math.sin(rhTheta)
    ey2 = ey - arrowLength * math.cos(rhTheta)
    ctx.move_to(ex2, ey2)
    ctx.line_to(ex, ey)
    ctx.stroke()

def arrowHead(ctx, pos, theta, length,  arrowLength = None, dtheta = 15 * RADIANS_PER_DEGREE):
    if arrowLength is None:
        arrowLength = length * 0.35
    sx, sy = pos
    ex = sx
    ey = sy
    
    lhTheta = theta + dtheta
    ex1 = ex - arrowLength * math.sin(lhTheta)
    ey1 = ey - arrowLength * math.cos(lhTheta)
    ctx.move_to(ex1, ey1)
    ctx.line_to(ex, ey)
    ctx.stroke()

    rhTheta = theta - dtheta
    ex2 = ex - arrowLength * math.sin(rhTheta)
    ey2 = ey - arrowLength * math.cos(rhTheta)
    ctx.move_to(ex2, ey2)
    ctx.line_to(ex, ey)
    ctx.stroke()


def red(ctx):
    ctx.set_source_rgb (1.0, 0.0, 0.0)

def green(ctx):
    ctx.set_source_rgb (0.0, 1.0, 0.0)

def cyan(ctx):
    ctx.set_source_rgb (0.0, 1.0, 1.0)

def blue(ctx):
    ctx.set_source_rgb (0.0, 0.0, 1.0)

def black(ctx):
    ctx.set_source_rgb (0.0, 0.0, 0.0)

def white(ctx):
    ctx.set_source_rgb (1.0, 1.0, 1.0)

