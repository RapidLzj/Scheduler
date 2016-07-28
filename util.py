# -*- coding: utf-8 -*-
"""
    Module util
    Utilities for common routine, can also be used in other task
    v1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    Providing:
        hms/dms to and from decimal
        sxpar, get value from fits header
        progress bar
        readconf, read configure file, remove comment and empty lines
"""

import os
import sys


def dms2dec ( dms, delimiter=":" ) :
    """ Transform deg:min:sec format angle to decimal format
    args:
        dms: sexagesimal angle string, format +/-dd:mm:ss.xxx
        delimiter: char seperate deg, min and sec, default is ":"
    returns:
        decimal angle in degree
    """
    pp = dms.split(delimiter)
    if len(pp) >= 3 :
        ss = float(pp[2])
    else :
        ss = 0.0
    if len(pp) >= 2 :
        mm = float(pp[1])
    else :
        mm = 0.0
    hh = abs(float(pp[0]))
    pm = -1.0 if dms[0] == "-" else 1.0

    dec = pm * (hh + mm / 60.0 + ss / 3600.0)
    return dec

def hms2dec ( hms, delimiter=":" ) :
    """ Transform hour:min:sec format angle to decimal format
    args:
        hms: sexagesimal angle string, format hh:mm:ss.xxx
        delimiter: char seperate deg, min and sec, default is ":"
    returns:
        decimal angle in degree
    """
    dec = dms2dec(hms, delimiter) * 15.0
    return dec


def dec2dms ( dec, len=11, delimiter=":" ) :
    """ Transform decimal format angle to deg:min:sec format
    args:
        dec: decimal angle in degree
        len: output length of string
        delimiter: char seperate deg, min and sec, default is ":"
    returns:
        sexagesimal angle string, format +/-dd:mm:ss.xxx
    """
    dec0 = dec % 360.0 if dec >= 0.0 else dec % -360.0
    pm = "-" if dec0 < 0.0 else "+"
    adec = abs(dec0)
    dd = int(adec)
    mm = int((adec - dd) * 60.0)
    ss = (adec - dd) * 3600 - mm * 60.0
    dms = "{n:1s}{d:02d}{l}{m:02d}{l}{s:08.5f}".format(n=pm, d=dd, m=mm, s=ss, l=delimiter)
    return dms[0:len]


def dec2hms ( dec, len=11, delimiter=":" ) :
    """ Transform decimal format angle to deg:min:sec format
    args:
        dec: decimal angle in degree
        len: output length of string
        delimiter: char seperate deg, min and sec, default is ":"
    returns:
        sexagesimal angle string, format hh:mm:ss.xxx
    """
    hh = (dec % 360.0) / 15.0
    hms = dec2dms(hh, len+1, delimiter)
    return hms[1:]


def hour2str ( hr, delimiter=":" ) :
    """ Transfer hours to hh:mm format string
    args:
        hr: hours, 0.0 to 36.0, will error for negative
        delimiter: char seperate deg, min and sec, default is ":"
    returns:
        string hours and minutes, in hh:mm format
    """
    mi = int(round(hr * 60))
    hh = int(mi / 60)
    mm = int(mi % 60)
    s = "{h:02d}{l}{m:02d}".format(h=hh, m=mm, l=delimiter)
    return s


def sxpar ( header, key, default=None ) :
    """ Check weather the key is in header, if yes, return value, else return default
    args:
        header: fits head, get from hdulist[x].header
        key: key of the card you want to visit
        default: default value if key not in header, and if key exists, but value is empty
    returns:
        value of key, if not exists or empty, return default value
    """
    if key in header.keys() :
        v = header[key]
        if v == "" :
            v = default
    else :
        v = default
    return v


def progress_bar ( value, v_to = 100, v_from = 0, length=80,
                   percent_format="{:>6.1%}", value_format="{:>5d}",
                   done_char="=", wait_char=" ") :
    """ Display a progress bar in line, and overwrite it on next display
    args:
        value: progress bar position value
        v_to: right end value of progress bar
        v_from: left end value of progress bar
        length: length of progress bar body, between []
        percent_format: format of percent display, set None to suppress diaplay
        value_format: format of value displan, set None to suppress display
        done_char: char of done part of progress bar, left part
        wait_char: char of waiting part of progress bar, right part
    """
    pcnt = (float(value) - v_from) / (v_to - v_from)
    pcnt = 0.0 if pcnt < 0.0 else 1.0 if pcnt > 1.0 else pcnt
    all_len = int(round(length))
    done_len = int(round(pcnt * all_len))
    wait_len = all_len - done_len
    done_str = done_char[0] * done_len
    wait_str = wait_char[0] * wait_len

    if percent_format is not None :
        sys.stdout.write(percent_format.format(pcnt))
    sys.stdout.write(" [{}{}] ".format(done_str, wait_str))
    if percent_format is not None :
        sys.stdout.write(value_format.format(value))
    sys.stdout.write("\r")
    sys.stdout.flush()

def read_conf ( conffile, default=None ) :
    """ Read configure file, and remove comments, empty lines
    args:
        conffile: configure file name
        default: default content if file not exists
    returns:
        a list of lines, leading and tailing space striped, empty line and comment removed
    """
    if os.path.isfile(conffile) :
        lines = open(conffile,"r").readlines()
    else :
        lines = default

    outlines = []
    for l in lines :
        k = l.split("#")[0].strip()
        if k != "" :
            outlines.append(k)

    return outlines


def msgbox ( msg, title="", border="+-|", width=80, align="" ) :
    """ Show message, and draw a box around the message
    args:
        msg: message text, a string or a string list/tuple
        title: a string show at the top of box
        border: border chars, 0 for corner, 1 for horizon, 2 for vertical
        width: outer width of the box, including the border
        align: alignment string, each char for the respective line
    returns:
        a message box, can be printed on screen or in file
    """
    if type(msg) == str :
        msg = [msg]
    if title is None or len(title.strip()) == 0 :
        title = ""
    else :
        title = " " + title.strip() + " "
    if border is None or len(border) == 0 :
        border = "+-|"
    elif len(border) == 1 :
        border = border * 3
    elif len(border) == 2 :
        border = border + border[1]
    else :
        border = border[0:3]
    align += "^" * len(msg)

    box = (border[0] + "{:" + border[1] + "^" + str(width-2) + "}" + border[0] + "\n").format(title)
    for m in range(len(msg)) :
        box += ("{0:1} {1:" + align[m] + str(width-4) + "} {0:1}\n").format(border[2], msg[m])
    box += (border[0] + "{:" + border[1] + "^" + str(width-2) + "}" + border[0] + "\n").format("")

    return box

