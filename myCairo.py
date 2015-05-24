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

def makeFillers( sIdx, sTup, endIdx, endTup):
    nums = arange( sIdx, endIdx + 1 )
    N = len(nums)
    reds   = linspace( sTup[0], endTup[0], N)
    greens = linspace( sTup[1], endTup[1], N)
    blues  = linspace( sTup[2], endTup[2], N)
    ret = {}
    for idx, r, g, b in zip( nums, reds, greens, blues):
        ret[idx] = (r,g,b)
    return ret

fillers = makeFillers( 18, (0.0, 0.0, 1.0), 30, (1.0, 0.0, 0.0) )


#fillers[0] = ( 1.0, 0.0, 1.0)
#fillers[8] = ( 0.0, 1.0, 0.0)

def ringBuffer(ctx,
               pos,
               outerRadius,
               innerRadius,
               segments,
               dutyCycle, fillers = {}):
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


outerR = 0.1
thickFactor = 0.8

surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context (surface)
ctx.set_source_rgb (0.3, 0.75, 0.75) # Solid color
ctx.set_line_width (0.004)
ctx.scale (WIDTH, HEIGHT) # Normalizing the canvas

ringBuffer(ctx, (0.5, 0.25) , outerR, outerR * thickFactor , 16, 0.8)
ringBuffer(ctx, (0.5, 0.5 ) , outerR, outerR * thickFactor , 16, 0.8)
surface.write_to_png ("example2.png") # Output to PNG

outerR = 0.05
thickFactor = 0.8
surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context (surface)
ctx.set_source_rgb (0.3, 0.75, 0.75) # Solid color
ctx.set_line_width (0.003)
ctx.scale (WIDTH, HEIGHT) # Normalizing the canvas

#text2(ctx, "foo", (0.5, 0.5) )

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

ctx.set_source_rgb (1.0, 1.0, 1.0)
arrow( ctx, (0.2, 0.25), 0.0, 0.3 - 0.05, 0.2 * 0.2)
ctx.set_source_rgb (0.0, 1.0, 0.0)
text2( ctx, "Orders", (0.27, 0.23), font_size = 0.025) 

ctx.set_line_width (0.0025)

blue(ctx)
ringBuffer(ctx, (0.5, 0.25), outerR, outerR * thickFactor , 12, 0.8)
ringBuffer(ctx, (0.5, 0.38), outerR, outerR * thickFactor , 12, 0.8)

black(ctx)

ctx.rectangle( 0.1, 0.1, 0.9, 0.9)

arrow( ctx, (0.2 + 0.3 - 0.05, 0.38), RADIANS_PER_DEGREE * 180, 0.3 - 0.05, 0.2 * 0.2)

green(ctx)
text2( ctx, "Executions", (0.27, 0.36), font_size = 0.025)

surface.write_to_png ("example3.png") # Output to PNG


outerR = 0.07
thickFactor = 0.8

surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)
ctx.set_line_width (0.002)
ctx.scale (WIDTH, HEIGHT) # Normalizing the canvas
ctx.set_source_rgb (1.0, 1.0, 1.0)
ctx.rectangle(0,0,1,1)
ctx.fill()
ctx.stroke()

def vec( pos, theta, r):
    x = pos[0] + r * math.sin(theta)
    y = pos[1] + r * math.cos(theta)
    return (x,y)

dx      = 30
angles  = [ RADIANS_PER_DEGREE * x for x in [ 270, 180, 90 ]   ]
centers = [ vec( (0.5, 0.5), theta , 0.35) for theta in angles ]

ARROW_LENGTH = 0.09
ARROW_GAP =0.02

arrowStarts  = [ vec( x , theta , outerR +  ARROW_GAP + ARROW_LENGTH ) for (x,theta) in zip(centers, angles) ]

arrowStarts2 = [ vec( x , theta + math.pi, outerR + ARROW_GAP) for (x,theta) in zip(centers, angles) ]

blue(ctx)

ctx.set_line_width (0.003)
for pos in centers:
    ringBuffer(ctx, pos, outerR, outerR * thickFactor , 16, 0.75)

black(ctx)

ctx.save()
ctx.set_line_width (0.006)
for (pos, theta) in zip(arrowStarts, angles):
    arrow(ctx, pos, theta + math.pi  , ARROW_LENGTH )

for (pos, theta) in zip(arrowStarts2, angles):
    arrow(ctx, pos, theta + math.pi  , ARROW_LENGTH )
ctx.restore()

if 0:
    ctx.new_path()
    ctx.move_to( arrowStarts[0][0],
                 arrowStarts[0][1])
    for pos in arrowStarts:
        x,y = pos
        ctx.line_to(x, y)
    ctx.close_path()
    ctx.stroke()

black(ctx)
rw, rh = 0.2, 0.15
ctx.save()
ctx.set_line_width (0.006)
ctx.arc( 0.5 , 0.5, 0.08, 0 * RADIANS_PER_DEGREE, 330 * RADIANS_PER_DEGREE)


endX = 0.5 + 0.08 * math.cos(330 * RADIANS_PER_DEGREE )
endY = 0.5 + 0.08 * math.sin(330 * RADIANS_PER_DEGREE )
arrow(ctx, (endX, endY), 330 * RADIANS_PER_DEGREE, 0.02)


ctx.stroke()
ctx.restore()

surface.write_to_png ("example4.png") # Output to PNG


def doSurf(SZ, dest, fillers = {}, SEGMENTS = 16):
    surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, SZ, SZ)
    ctx = cairo.Context(surface)
    ctx.set_line_width (0.01)
    ctx.scale (SZ, SZ) # Normalizing the canvas
    ctx.set_source_rgb (1.0, 1.0, 1.0)
    ctx.rectangle(0,0,1,1)
    ctx.fill()
    ctx.stroke()
    black(ctx)
    ringBuffer(ctx, (0.5, 0.5), 0.4, 0.8 * 0.4 , SEGMENTS, 0.75, fillers = fillers)
    surface.write_to_png (dest) # Output to PNG
doSurf(300, "example5.png")

doSurf(150, "trading_inout_queue.png")


doSurf(600, "example6.png", fillers = fillers, SEGMENTS = 32)

def doCont(SZ, dest):
    surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, SZ, SZ)
    ctx = cairo.Context(surface)
    ctx.set_line_width (0.01)
    ctx.scale (SZ, SZ) # Normalizing the canvas
    ctx.set_source_rgb (1.0, 1.0, 1.0)
    ctx.rectangle(0,0,1,1)
    ctx.fill()
    ctx.stroke()
    black(ctx)
    x = 0.05
    dx = 0.085
    dy = dx
    y = 0.1
    while x < 0.9:
        ctx.move_to (x, y)
        ctx.line_to (x + dx, y)
        ctx.line_to (x + dx, y + dy)
        ctx.line_to (x , y + dy)
        ctx.line_to (x , y )
        ctx.line_to (x + dx, y)
        ctx.stroke()
        x += 0.1

    #ctx.rectangle(0.1, 0.1, 0.3, 0.3)
        
    #ringBuffer(ctx, (0.5, 0.5), 0.4, 0.8 * 0.4 , 16, 0.75)
    print "Boom"
    surface.write_to_png (dest) # Output to PNG

doCont(150, "example7.png")

# Looper
surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, 300,300)
ctx = cairo.Context(surface)
ctx.set_line_width (0.01)
ctx.scale (300, 300) # Normalizing the canvas
ctx.set_source_rgb (1.0, 1.0, 1.0)
ctx.rectangle(0,0,1,1)
ctx.fill()
ctx.stroke()
black(ctx)
rw, rh = 0.2, 0.15
ctx.save()
ctx.arc( 0.5 , 0.5, 0.4, 0 * RADIANS_PER_DEGREE, 330 * RADIANS_PER_DEGREE)

endX = 0.5 + 0.4 * math.cos(330 * RADIANS_PER_DEGREE )
endY = 0.5 + 0.4 * math.sin(330 * RADIANS_PER_DEGREE )
arrowHead(ctx, (endX, endY), 38 * RADIANS_PER_DEGREE, 0.4)
surface.write_to_png ("example8.png") # Output to PNG


# Looper
surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, 500,500)
ctx = cairo.Context(surface)
ctx.set_line_width (0.01)
ctx.scale (500,500) # Normalizing the canvas
ctx.set_source_rgb (1.0, 1.0, 1.0)
ctx.rectangle(0,0,1,1)
ctx.fill()
ctx.stroke()
black(ctx)
rw, rh = 0.2, 0.15
ctx.save()
ctx.arc( 0.5 , 0.5, 0.4, 0 * RADIANS_PER_DEGREE, 330 * RADIANS_PER_DEGREE)

endX = 0.5 + 0.4 * math.cos(330 * RADIANS_PER_DEGREE )
endY = 0.5 + 0.4 * math.sin(330 * RADIANS_PER_DEGREE )
arrowHead(ctx, (endX, endY), 38 * RADIANS_PER_DEGREE, 0.4)
surface.write_to_png ("example9.png") # Output to PNG


