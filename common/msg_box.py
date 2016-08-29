# -*- coding: utf-8 -*-
"""
    2016-08-06, 2016M-1.0 lzj
    Utilities for pipeline, general operations
    Class msg_box, providing box
"""


class msg_box (object) :
    """ A class to generate a box, contains messages, can be printed
        Use a class will need extra statement, but an object can be used for many box
    """

    def __init__(self, border="+-|", width=80, align="") :
        """ Box init parameters
        args:
            border: border chars
            width: width of box, including border
            align: default align of lines
        """
        self._border = border
        self._width = width
        self._align = align

    def box(self, msg, title="", border=None, width=None, align=None) :
        """ Generate a box
        args:
            msg: message, a string or a string list/tuple
            title: title of box
            border: border chars, if None, use default at init
            width: width of box, including border, if None, use default at init
            align: default align of lines, if None, use default at init
        returns:
            box, as a string list
        """
        # make msg a list or a tuple
        if type(msg) == str :
            msg = [msg]
        # process title
        if title is None or len(title.strip()) == 0 :
            title = ""
        else :
            title = " " + title.strip() + " "
        # process border
        if border is None or len(border) == 0 :
            border = self._border
        elif len(border) == 1 :
            border *= 3
        elif len(border) == 2 :
            border += border[1]
        # process width
        if width is None : width = self._width
        # process align
        if align is None or len(align.strip()) == 0 : align = self._align
        if align is None or align == "" : align = "^"
        if len(align) < len(msg) : align *= int(len(msg) / len(align) + 1)

        out = []
        out.append((border[0] + "{:" + border[1] + "^" + str(width-2) + "}" + border[0]).format(title))
        for m in range(len(msg)) :
            out.append(("{0:1} {1:" + align[m] + str(width-4) + "} {0:1}").format(border[2], msg[m]))
        out.append((border[0] + "{:" + border[1] + "^" + str(width-2) + "}" + border[0]).format(""))

        return out

