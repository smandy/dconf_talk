#!/usr/bin/env python

import math
import cairo

from cairoLib import black, white as setWhite
from collections import defaultdict

WIDTH, HEIGHT = 800,600
RADIANS_PER_DEGREE = 2 * math.pi / 360

def text(ctx,
         string,
         pos,
         theta = 0.0,
         face = 'Ubuntu',
         font_size = 12):
    ctx.select_font_face(face , cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(font_size)
    #nx = -tw/2.0
    #ny = fheight/2
    ctx.move_to(pos[0], pos[1])
    ctx.show_text(string)
    ctx.stroke()

def doRect(ctx, x,y, sz, fillWith = None, border = True):
    if fillWith is not None:
        ctx.set_source_rgb (*fillWith)
        ctx.rectangle(x,y, sz, sz)
        ctx.fill()
        ctx.stroke()
    if border:
        black(ctx)
        ctx.rectangle(x,y, sz,sz)
        ctx.stroke()

def makeContext(fn):
    surface = cairo.SVGSurface (fn, WIDTH, HEIGHT)
    ctx = cairo.Context (surface)
    setWhite(ctx)
    #ctx.scale (WIDTH, HEIGHT) # Normalizing the canvas
    ctx.rectangle(0,0,WIDTH, HEIGHT)
    ctx.fill()
    ctx.stroke()
    ctx.set_line_width (1.5)
    return ctx, surface

cyan        = (0  , 1.0 , 1.0)
dark_cyan   = (0  , 0.7 , 0.7)
blue = (0,0,1)

yellow = (1.0, 1.0 ,   0)
red    = (1  ,   0 ,   0)
green = (0,1,0)

def fromRgb(s):
    """Read strings produced by helm color"""
    import re
    return tuple([ int(x, 16)/255.0 for x in re.findall('..', s[1:]) ])

seaGreen = fromRgb('#20b2aa')
grey     = fromRgb('#696969')
magenta  = fromRgb('#Ff00ff')
orange   = fromRgb('#Ff8c00')
white  = (1  ,   1, 1)

from itertools import izip, count

starty = 30
startx = 30

BOX_WIDTH = 10

def makeLegend(ctx, xy, labels, bs = 20 ):
    x, y = xy
    for i, (c,label) in enumerate(labels):
        doRect( ctx, x, y, bs, c)
        text( ctx, label, (x + 30, y + 12))
        y += 1.5 * bs

colours = 14 * [ green] + 8 * [orange] + 8 * [ blue ] + 6 * [ cyan ] + 6 * [yellow] + 8 * [seaGreen]

labels = [
    ( green , 'wmp1'),
    ( orange , 'wmp2'),
    ( blue  , 'wmp3'),
    ( cyan  , 'wmp4'),
    ( yellow, 'wmp5'),
    ( seaGreen, 'wmp6'),
    ( red     , 'private fill') ]
    
def dullen(c):
    return tuple( [ x * 0.5 for x in c ])


def makeChart(fn,
              staggers,
              fillColumn,
              filterNonEvents = False,
              drawSlices = False,
              drawLegend = False, ts = None):
    fillColumns = [3,12, 17,20, 28]
    ctx, surface = makeContext('%s.svg' % fn)
    colorsForX = defaultdict(list)
    offsetsFor = {}
    isFillColumn = {}
    
    startx = 30 + (len(staggers) - fillColumn) * BOX_WIDTH
    for stagger,yoffset in izip(staggers, count() ):
        y = starty + yoffset * BOX_WIDTH
        for i, colour in enumerate(colours):
            x = startx + ( i -  stagger) * BOX_WIDTH
            isFill = i in fillColumns
            if yoffset == fillColumn:
                if isFill:
                    isFillColumn[x] = True
                    offsetsFor[i] = x

    for stagger, yoffset in izip(staggers, count()):
        #print "stagger", stagger
        y = starty + yoffset * BOX_WIDTH
        for i, colour in enumerate(colours):
            x = startx + (i -  stagger) * BOX_WIDTH
            isFill = i in fillColumns
            if yoffset == fillColumn:
                if isFill:
                    c = red
                    offsetsFor[i] = x
                else:
                    c = white
            else:
                c = colour
            colorsForX[x].append(c)
            if isFillColumn.get(x, False) or not filterNonEvents:
                doRect( ctx, x, y, BOX_WIDTH, c)
            else:
                doRect( ctx, x, y, BOX_WIDTH, dullen(c) )
        if stagger<0:
            s = "t-%s" % abs(stagger)
        elif stagger==0:
            s = "t"
        else:
            s = "t+%s" % stagger
        text( ctx, s, (10, y))
        print "Added", s, 0, y

    if drawSlices:
        x0 , y = drawSlices

        for i, column in enumerate(fillColumns):
            x = x0 + 60
            text( ctx, "Fill %s" % (i+1), (x0, y+15) )
            colors = colorsForX[offsetsFor[column]]
            #print colors
            bw2 = 20
            for c in colors:
                doRect( ctx, x, y, bw2, c)
                x += bw2
            y += 2 * bw2

    ctx.stroke()
    if drawLegend:
        makeLegend(ctx, drawLegend, labels)

    surface.write_to_png ("%s.png" % fn) # Output to PNG
    surface.finish()

fc = 3
tzero = 20 - fc
staggers = range(-fc, 0) + [0,0] + range(1,20)
#fullStaggers = range(fc) + [fc] + range(fc,20)

makeChart( 'pfe1', [0,0], 0, drawLegend = (450,80))
makeChart( 'pfe2', [0] * 20, fc, drawLegend = (50, 260))
makeChart( 'pfe3', staggers, fc, drawLegend = (50, 260))

makeChart( 'pfe4', staggers, fc,
           filterNonEvents = True,
           drawSlices = ( 25,310),
           drawLegend = (650, 300))
