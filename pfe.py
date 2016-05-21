#!/usr/bin/env python

import math
import cairo

from cairoLib import black, white as setWhite

WIDTH, HEIGHT = 800,600
RADIANS_PER_DEGREE = 2 * math.pi / 360
def text(ctx,
         string,
         pos,
         theta = 0.0,
         face = 'Ubuntu',
         font_size = 12):
    ctx.save()
    ctx.select_font_face(face , cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(font_size)
    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    x_off, y_off, tw, th = ctx.text_extents(string)[:4]
    #nx = -tw/2.0
    #ny = fheight/2

    ctx.translate(pos[0], pos[1])
    ctx.rotate(theta)
    #ctx.translate(nx, ny)
    ctx.move_to(0,0)
    ctx.show_text(string)
    ctx.restore()

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
    #surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    surface = cairo.SVGSurface (fn, WIDTH, HEIGHT)
    ctx = cairo.Context (surface)
    setWhite(ctx)
    #ctx.scale (WIDTH, HEIGHT) # Normalizing the canvas
    ctx.rectangle(0,0,WIDTH, HEIGHT)
    ctx.fill()
    ctx.stroke()
    ctx.set_line_width (1.5)
    return ctx, surface


def fromRgb(s):
    """Read strings produced by helm color"""
    import re
    return tuple([ int(x, 16)/255.0 for x in re.findall('..', s[1:]) ])


#print fromRgb('#Ff8c00')

cyan        = (0  , 1.0 , 1.0)
dark_cyan   = (0  , 0.7 , 0.7)
blue = (0,0,1)

seaGreen = fromRgb('#20b2aa')
yellow = (1.0, 1.0 ,   0)
red    = (1  ,   0 ,   0)
green = (0,1,0)

grey = fromRgb('#696969')

magenta = fromRgb('#Ff00ff')
white  = (1  ,   1, 1)
orange = fromRgb('#Ff8c00')

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

colours = 14 * [ green] + 8 * [orange] + 8 * [ blue ] + 6 * [ cyan ] + 6 * [yellow] + 14 * [seaGreen]

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

from collections import defaultdict

def makeChart(fn,
              staggers,
              fillColumn,
              filterNonEvents = False,
              drawSlices = False,
              drawLegend = False):
    fillColumns = [11,15, 20,26, 35]
    ctx, surface = makeContext('%s.svg' % fn)
    colorsForX = defaultdict(list)
    offsetsFor = {}
    isFillColumn = {}
    for stagger,yoffset in izip(reversed(staggers), count() ):
        y = starty + yoffset * BOX_WIDTH
        for i, colour in enumerate(colours):
            x = startx + (i + stagger) * BOX_WIDTH
            isFill = i in fillColumns
            if yoffset == fillColumn:
                if isFill:
                    isFillColumn[x] = True
                    offsetsFor[i] = x

    for stagger,yoffset in izip(reversed(staggers), count() ):
        #x = startx + stagger * BOX_WIDTH
        y = starty + yoffset * BOX_WIDTH
        tminus = yoffset - fillColumn
        if tminus < 0:
            s = "t-%s" % abs(tminus)
        elif tminus==0:
            s = "t"
        else:
            s = "t+%s" % tminus
            
        text(ctx, s, (0, y))

        for i, colour in enumerate(colours):
            x = startx + (i + stagger) * BOX_WIDTH
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
                

    #BOX_WIDTH = 20
    if drawSlices:
        x0 , y = drawSlices

        for i, column in enumerate(fillColumns):
            x = x0 + 60
            text( ctx, "Fill %s" % (i+1), (x0, y+15) )
            colors = colorsForX[offsetsFor[column]]
            print colors
            bw2 = 20
            for c in colors:
                doRect( ctx, x, y, bw2, c)
                x += bw2

                
            y += 2 * bw2

    if drawLegend:
        makeLegend(ctx, drawLegend, labels)

    surface.write_to_png ("%s.png" % fn) # Output to PNG
    surface.finish()

fc = 3
    
makeChart( 'pfe1', [0,0], 0, drawLegend = (450,80))
makeChart( 'pfe2', [0] * 20, fc, drawLegend = (50, 260))
makeChart( 'pfe3', range(fc) + [fc] + range(fc,20), fc, drawLegend = (50, 260))
makeChart( 'pfe4', range(fc) + [fc] + range(fc,20), fc,
           filterNonEvents = True,
           drawSlices = ( 50,280),
           drawLegend = (600, 280))
