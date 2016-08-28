# -*- coding: utf-8 -*-
"""
    Module headerinfo : part of SAGE Digital Sky Survey Observation Scheduler
    v 1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    This function used to collect observation basic info from header of fits.
    Use it to make fits from different telescope works likely.
"""


import os
import numpy as np
from astropy.io import fits
import common
import schdutil


def headerinfo ( fitsfile ) :
    """ Get info from fits header
    args:
        fitsfile: fits filename, with full path
    return:
        instance of class schdutil.check_info
    """
    if not os.path.isfile(fitsfile) :
        return None

    # open file and get primary header
    hdulist = fits.open(fitsfile)
    prihdr = hdulist[0].header

    telescope = prihdr["TELESCOP"].strip()
    if telescope == "Steward 2.3 m (bok)" :
        filesn = int(fitsfile[-9:-5])
        imgtyp = common.util.sxpar(prihdr, "IMAGETYP", "unknown")
        object = common.util.sxpar(prihdr, "OBJECT", "unknown")
        filter = common.util.sxpar(prihdr, "FILTER", "unknown")
        expt   = float(common.util.sxpar(prihdr, "EXPTIME", 0.0))
        ra = common.angle.hms2dec(common.util.sxpar(prihdr, "RA", "0"))
        de = common.angle.dms2dec(common.util.sxpar(prihdr, "DEC", "0"))
        res = schdutil.check_info(fitsfile, filesn, imgtyp, object, filter, expt, ra, de)

    elif telescope == "1M-WideField" :
        filesn = int(fitsfile[-9:-5])
        imgtyp = common.util.sxpar(prihdr, "OBSTYPE", "unknown")
        object = common.util.sxpar(prihdr, "OBJECT", "unknown")
        filter = common.util.sxpar(prihdr, "FILTER", "unknown")
        expt   = float(common.util.sxpar(prihdr, "EXPTIME", 0.0))
        ra = float(common.util.sxpar(prihdr, "OBJCTRA", 0.0))
        de = float(common.util.sxpar(prihdr, "OBJCTDEC", 0.0))
        res = schdutil.check_info(fitsfile, filesn, imgtyp, object, filter, expt, ra, de)

    else :
        res = None

    hdulist.close()
    return res

if __name__ == "__main__" :
    pass
