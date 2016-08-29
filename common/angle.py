# -*- coding: utf-8 -*-
"""
    2016-06-17, 2016M-1.0 lzj
    Utilities for pipeline, general operations
    This part including angle operations
"""


def dms2dec (dms, delimiter=":") :
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


def hms2dec (hms, delimiter=":") :
    """ Transform hour:min:sec format angle to decimal format
    args:
        hms: sexagesimal angle string, format hh:mm:ss.xxx
        delimiter: char seperate deg, min and sec, default is ":"
    returns:
        decimal angle in degree
    """
    dec = dms2dec(hms, delimiter) * 15.0
    return dec


def dec2dms (dec, len=11, delimiter=":") :
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


def dec2hms (dec, len=11, delimiter=":") :
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


def hour2str (hr, delimiter=":") :
    """ Transfer hours to hh:mm format string
    args:
        hr: hours, 0.0 to 36.0, will error for negative
        delimiter: char separate deg, min and sec, default is ":"
    returns:
        string hours and minutes, in hh:mm format
    """
    mi = int(round(hr * 60))
    hh = int(mi / 60)
    mm = int(mi % 60)
    s = "{h:02d}{l}{m:02d}".format(h=hh, m=mm, l=delimiter)
    return s


def angle_dis (a1, a2, factor=1.0) :
    """ Get distance between angles, around 360-degree bound
    args:
        a1: angle 1, scalar or ndarray
        a2: angle 2, scalar or ndarray, if both a1 and a2 are ndarray, they must have same shape
        factor: a shrink factor, usually is 1.0/cos(dec) or 1.0/cos(lat)
    returns:
        distance between a1 and a2
    """
    d = ((a1 - a2 + 180.0) % 360.0 - 180.0) * factor
    return d
