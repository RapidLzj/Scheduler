# -*- coding: utf-8 -*-
"""
    Module plotmap : part of SAGE Digital Sky Survey Observation Scheduler
    v 1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    Draw a sky map.
"""


import numpy as np
from myPyLib.Mollweide import moll
from matplotlib import pyplot as plt
import util
import schdutil


def plotmap (ra, de, tag, title="", epsfile=None, pngfile=None,
             spos=None, mpos=None, zenith=None,
             xcolormark=None, xlabel=None) :
    """ Plot a map about fields, different tag have different color and marker.
    args:
        ra: ndarray of ra
        de: ndarray of dec
        tag: ndarray of tag
        title: title of map
        epsfile: eps filename to save, if None, do not save as eps
        pngfile: png filename to save, if None, do not save as png
        mpos: tuple of ra and dec of moon position, if none, do not mark
        spos: tuple of ra and dec of sun position, if none, do not mark
        zenith: tuple of ra and dec of zenith, if none, do not mark
        xcolormark: dict of color and mark for different tag, if none, use default
        xlabel: dict of labels for each tag, if none, use default
    """

    # handling default arguments
    if xcolormark is None :
        xcolormark = {
            0x00:"k,",  # unobserved and not planed
            0x01:"k+",  # partly observed and not planned
            0x02:"go",  # finished
            0x03:"rs",  # planed in this night
            0x04:"m+",  # candidate0
            0x05:"m+",  # candidate1
            0x07:"bs",  # latest added
            0x10:"y,",  # Sun or Moon neighbourhood
            0x11:"y+",  #
            0x12:"yo",  #
            }
    if xlabel is None :
        xlabel = {
            0x00:"Unobserved",
            0x01:"Partly obsed",
            0x02:"Finished",
            0x03:"Tonight",
            0x04:"Candidate",
            0x05:None,
            0x07:"New Selection",
            0x10:"Near Sun/Moon",
            0x11:"Near Sun/Moon",
            0x12:"Near Sun/Moon"
            }

    # plot
    equf = moll(lat_range=(-5,88), xsize=180, ysize=90, lon_center=30.0)
    plt.figure(figsize=(18,10))

    equf.grid(lat_lab_lon=240, lon_lab_lat=-5, lat_step=10)
    for t in set(tag):
        ix = np.where(tag == t)
        equf.scatter(ra[ix], de[ix], xcolormark[t], label=xlabel[t])
    if spos is not None :
        x, y = equf.project(spos[0], spos[1])
        plt.plot(x, y, "ro", markersize=10.0,
            label="Sun {ra:5.1f} {de:5.1f}".format(ra=spos[0], de=spos[1]))
    if mpos is not None :
        x, y = equf.project(mpos[0], mpos[1])
        plt.plot(x, y, "rD", markersize=10.0,
            label="Moon {ra:5.1f} {de:5.1f}".format(ra=mpos[0], de=mpos[1]))
    if zenith is not None :
        x, y = equf.project(zenith[0], zenith[1])
        plt.plot(x, y, "r^", markersize=10.0,
            label="Zenith {ra:5.1f} {de:5.1f}".format(ra=zenith[0], de=zenith[1]))

    plt.legend()
    plt.title("{title} Observation Plan".format(title=title))

    if epsfile is not None : plt.savefig(epsfile)
    if pngfile is not None : plt.savefig(pngfile)
    plt.close()
