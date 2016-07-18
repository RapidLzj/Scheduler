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


def headerinfo ( fitsfile ) :
    """ Get info from fits header
    param fitsfile: fits filename, with full path
    return: dict of (filename, filesn, imagetype,
    object, filter, exposure time seconds, ra deg, dec deg)
    """
    if not os.path.isfile(fitsfile) :
        return None

    # open file and get primary header
    hdulist = fits.open(fitsfile)
    prihdr = hdulist[0].header

    telescope = prihdr["TELESCOP"].strip()
    if telescope == "Steward 2.3 m (bok)" :
        filesn = int(fitsfile[-9:-5])
        imgtyp = prihdr["IMAGETYP"].strip()
        object = prihdr["OBJECT"].strip()
        filter = prihdr["FILTER"].strip()
        expt   = float(prihdr["EXPTIME"])
        radeg  = util.hms2dec(prihdr["RA"].strip())
        decdeg = util.dms2dec(prihdr["DEC"].strip())
        res = {"filename": fitsfile,
               "filesn": filesn,
               "imagetype": imgtyp,
               "object": object,
               "filter": filter,
               "exptime": expt,
               "ra": radeg,
               "dec": decdeg }

    elif telescope == "1M-WideField" :
        filesn = int(fitsfile[-9:-5])
        imgtyp = prihdr["OBSTYPE"].strip()
        object = prihdr["OBJECT"].strip()
        filter = prihdr["FILTER"].strip()
        expt   = float(prihdr["EXPTIME"].strip())
        radeg  = float(prihdr["OBJCTRA"].strip())
        decdeg = float(prihdr["OBJCTDEC"].strip())
        res = {"filename": fitsfile,
               "filesn": filesn,
               "imagetype": imgtyp,
               "object": object,
               "filter": filter,
               "exptime": expt,
               "ra": radeg,
               "dec": decdeg }

    else :
        res = None

    hdulist.close()
    return res

if __name__ == "__main__" :
    pass