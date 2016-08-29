# -*- coding: utf-8 -*-
"""
    2016-06-17, 2016M-1.0 lzj
    Constants for pipeline, general operations
    This part providing some constants, necessary for pipeline, but common between telescopes.
"""


import numpy as np


class com_const (object) :
    """ A static class, providing constants
    """

    # record structure of catalog : [(name, type, unit, disp)]
    cata_cols = [("starno",    np.int32,   "J", "No",  "5d"),
                 ("mjd",       np.int16,   "I", "DAY", "04d"),
                 ("fileno",    np.int16,   "I", "NO",  "04d"),
                 ("filter",    np.str_,    "8A","",    "8s"),
                 ("x",         np.float32, "E", "PIX", "10.5f"),
                 ("y",         np.float32, "E", "PIX", "10.5f"),
                 ("elong",     np.float32, "E", "",    "5.3f"),
                 ("fwhm",      np.float32, "E", "PIX", "6.3f"),
                 ("mag_auto",  np.float32, "E", "MAG", "6.3f"),
                 ("err_auto",       np.float32, "E", "MAG", "6.4f"),
                 ("mag_best",  np.float32, "E", "MAG", "6.3f"),
                 ("err_best",  np.float32, "E", "MAG", "6.4f"),
                 ("mag_petro", np.float32, "E", "MAG", "6.3f"),
                 ("err_petro", np.float32, "E", "MAG", "6.4f"),
                 ("mag_aper1", np.float32, "E", "MAG", "6.3f"),
                 ("err_aper1", np.float32, "E", "MAG", "6.4f"),
                 ("mag_aper2", np.float32, "E", "MAG", "6.3f"),
                 ("err_aper2", np.float32, "E", "MAG", "6.4f"),
                 ("mag_aper3", np.float32, "E", "MAG", "6.3f"),
                 ("err_aper3", np.float32, "E", "MAG", "6.4f"),
                 ("mag_aper4", np.float32, "E", "MAG", "6.3f"),
                 ("err_aper4", np.float32, "E", "MAG", "6.4f"),
                 ("mag_aper5", np.float32, "E", "MAG", "6.3f"),
                 ("err_aper5", np.float32, "E", "MAG", "6.4f"),
                 ("flags",     np.uint8,   "B", "",    "8b"),
                 ("mag_corr",  np.float32, "E", "MAG", "6.3f"),
                 ("err_corr",  np.float32, "E", "MAG", "6.4f"),
                 ("radeg",     np.float64, "D", "DEG", "10.6f"),
                 ("decdeg",    np.float64, "D", "DEG", "10.6f"),
                 ("raerr",     np.float32, "E", "SEC", "5.2f"),
                 ("decerr",    np.float32, "E", "SEC", "5.2f"),
                 ("rastr",     np.str_,    "11A","HMS","11s"),
                 ("decstr",    np.str_,    "11A","DMS","11s"),
                 ("ixwcs",     np.int32,   "J",  "NO", "5d"),
                 ("ixmag",     np.int32,   "J",  "NO", "5d"),
                 ("ampno",     np.int8,    "B",  "NO", "2d"),
                 ]
    #cata_dtype = [(c[0], c[1]) for c in cata_cols]

