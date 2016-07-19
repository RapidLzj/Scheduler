"""
    Module headerinfo : part of SAGE Digital Sky Survey Observation Scheduler
    v 1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    This function used to collect observation basic info from header of fits.
    Use it to make fits from different telescope works likely.
"""


import os
import numpy as np
from astropy.io import fits
import util
import schdutil


def headerinfo ( fitsfile ) :
    """ Get info from fits header
    param fitsfile: fits filename, with full path
    return: instance of class schdutil.check_info
    """
    if not os.path.isfile(fitsfile) :
        return None

    # open file and get primary header
    hdulist = fits.open(fitsfile)
    prihdr = hdulist[0].header

    telescope = prihdr["TELESCOP"].strip()
    if telescope == "Steward 2.3 m (bok)" :
        filesn = int(fitsfile[-9:-5])
        imgtyp = util.sxpar(prihdr, "IMAGETYP", "unknown")
        object = util.sxpar(prihdr, "OBJECT", "unknown")
        filter = util.sxpar(prihdr, "FILTER", "unknown")
        expt   = float(util.sxpar(prihdr, "EXPTIME", 0.0))
        radeg  = util.hms2dec(util.sxpar(prihdr, "RA", "0"))
        decdeg = util.dms2dec(util.sxpar(prihdr, "DEC", "0"))
        #res = {"filename": fitsfile,
        #       "filesn": filesn,
        #       "imagetype": imgtyp,
        #       "object": object,
        #       "filter": filter,
        #       "exptime": expt,
        #       "ra": radeg,
        #       "dec": decdeg }
        res = schdutil.check_info(fitsfile, filesn, imgtyp, object, filter, expt, radeg, decdeg)

    elif telescope == "1M-WideField" :
        filesn = int(fitsfile[-9:-5])
        imgtyp = util.sxpar(prihdr, "OBSTYPE", "unknown")
        object = util.sxpar(prihdr, "OBJECT", "unknown")
        filter = util.sxpar(prihdr, "FILTER", "unknown")
        expt   = float(util.sxpar(prihdr, "EXPTIME", 0.0))
        radeg  = float(util.sxpar(prihdr, "OBJCTRA", 0.0))
        decdeg = float(util.sxpar(prihdr, "OBJCTDEC", 0.0))
        #res = {"filename": fitsfile,
        #       "filesn": filesn,
        #       "imagetype": imgtyp,
        #       "object": object,
        #       "filter": filter,
        #       "exptime": expt,
        #       "ra": radeg,
        #       "dec": decdeg }
        res = schdutil.check_info(fitsfile, filesn, imgtyp, object, filter, expt, radeg, decdeg)

    else :
        res = None

    hdulist.close()
    return res

if __name__ == "__main__" :
    pass
