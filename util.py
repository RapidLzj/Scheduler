"""
    Module util
    Utilities for Scripts
    v1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    Providing: hms/dms to and from decimal
"""


def dms2dec ( dms ) :
    """ Transform deg:min:sec format angle to decimal format
    """
    pp = dms.split(":")
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

def hms2dec ( hms ) :
    """ Transform hour:min:sec format angle to decimal format
    """
    dec = dms2dec(hms) * 15.0
    return dec

def dec2dms ( dec, len=11 ) :
    """ Transform decimal format angle to deg:min:sec format
    """
    pm = "-" if dec < 0.0 else "+"
    adec = abs(dec)
    dd = int(adec)
    mm = int((adec - dd) * 60.0)
    ss = (adec - dd) * 3600 - mm * 60.0
    dms = "{0:1s}{1:0>2d}:{2:0>2d}:{3:0>7.4f}".format(pm, dd, mm, ss)
    return dms[0:len]

def dec2hms ( dec, len=11 ) :
    """ Transform decimal format angle to deg:min:sec format
    """
    hms = dec2dms(dec/15.0, len+1)
    return hms[1:]
