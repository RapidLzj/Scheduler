# -*- coding: utf-8 -*-
"""
    2016-08-06, 2016M-1.0 lzj
    Utilities for pipeline, general operations
    Catalog process, rotate, input, output.
"""


def rotate(x, y, ctx, cty, ang) :
    """ Rotate catalog x,y against center (ctx,cty), using specified rotate angle
    args:
        x: ndarray of x, or scalar
        y: ndarray of y
        ctx: center x, scalar
        cty: center y
        ang: rotate angle, 0-7
            0 keep original
            1 CW 90 deg
            2 180 deg
            3 CW 270 deg (CCW 90 deg)
            4 mirror leftup - rightdown
            5 mirror x
            6 mirror leftdown - rightup
            7 mirror y
    returns:
        tuple of newx,newy
    """
    ang %= 8
    x -= ctx
    y -= cty

    if ang == 1 : # CW 90 deg
        rx = +y
        ry = -x
    elif ang == 2 : # 180 deg
        rx = -x
        ry = -y
    elif ang == 3 : # CW 270 deg (CCW 90 deg)
        rx = -y
        ry = +x
    elif ang == 4 : # mirror leftup - rightdown
        rx = +y
        ry = +x
    elif ang == 5 : # mirror x
        rx = -x
        ry = +y
    elif ang == 6 : # mirror leftdown - rightup
        rx = -y
        ry = -x
    elif ang == 7 : # mirror y
        rx = +x
        ry = -y
    else : # 0, keep original
        rx = +x
        ry = +y

    rx += ctx
    ry += cty

    return rx, ry
