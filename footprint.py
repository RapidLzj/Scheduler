#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Module footprint : part of SAGE Digital Sky Survey Observation Scheduler
    v 1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    This function draw footprint of specified run, day and plan
"""


import os
import sys
import time
from Mollweide import moll
from matplotlib import pyplot as plt
import common
import schdutil


def footprint (tel, reportfile=None, equfile=None, galfile=None,
               run=None, day=None, before=False) :
    """ Draw footprint of survey
    args:
        tel: telescope brief code
        reportfile: report text file, default is current datetime,
                    set empty string will suppress output, same for figure file
        equfile: output file name for Equatorial System
        galfile: output file name for Galactic System
        run: code of run to be marked, usually as yyyymm format
        day: mjd of date to be marked, must be present with run
        before: draw covered bofore specified run or day
    """
    # set default output file
    dt = time.strftime("%Y%m%d%H%M%S")
    if reportfile is None :
        reportfile = "{tel}/obsed/footprint/report.{dt}.txt".format(tel=tel, dt=dt)
    if equfile is None :
        equfile = "{tel}/obsed/footprint/equ.{dt}.png".format(tel=tel, dt=dt)
    if galfile is None :
        galfile = "{tel}/obsed/footprint/gal.{dt}.png".format(tel=tel, dt=dt)

    # load fields configure file
    plans  = schdutil.load_expplan(tel)
    fields = schdutil.load_field(tel)
    plancode = list(plans.keys())
    plancode.sort()

    # find all obsed file
    obsedlist = schdutil.ls_files("{tel}/obsed/*/obsed.J*.lst".format(tel=tel))

    if run is not None and day is not None :
        marklist = schdutil.ls_files("{tel}/obsed/{run}/obsed.J{day:0>4d}.lst".format(tel=tel, run=run, day=day))
        marktext = "J{day:0>4d}".format(run=run, day=day)
    elif run is not None and day is None :
        marklist = schdutil.ls_files("{tel}/obsed/{run}/obsed.J*.lst".format(tel=tel, run=run))
        marktext = "{run}".format(run=run, day=day)
    else :
        marklist = []
        marktext = None

    if before :
        maxmark = max(marklist)
        obsedlist = [f for f in obsedlist if f <= maxmark]

    schdutil.load_obsed(fields, obsedlist, plans, marklist)

    # generate a text report
    if reportfile != "" :
        with open(reportfile, "w") as rep :
            for f in fields.values() :
                rep.write(("{0}  {1:1d} ").format(f, f.tag))
                for p in plancode :
                    rep.write(" {:>4.1f}".format(f.factor[p]))
                for p in plancode :
                    rep.write(" {:>4.1f}".format(f.mark[p]))
                rep.write("\n")
        #rep.close()

    # draw Equatorial System
    plt.rcParams['figure.figsize'] = 16,10
    # extract ra/dec/gl/gb from fields, by different tag
    # use np.where can do this better, but I am lazy
    ra0 = [f.ra for f in fields.values() if f.tag == 0]
    de0 = [f.de for f in fields.values() if f.tag == 0]
    gl0 = [f.gl for f in fields.values() if f.tag == 0]
    gb0 = [f.gb for f in fields.values() if f.tag == 0]
    n0 = len(ra0)
    ra1 = [f.ra for f in fields.values() if f.tag == 1 or f.tag == 2]
    de1 = [f.de for f in fields.values() if f.tag == 1 or f.tag == 2]
    gl1 = [f.gl for f in fields.values() if f.tag == 1 or f.tag == 2]
    gb1 = [f.gb for f in fields.values() if f.tag == 1 or f.tag == 2]
    n1 = len(ra1)
    ra3 = [f.ra for f in fields.values() if f.tag == 3]
    de3 = [f.de for f in fields.values() if f.tag == 3]
    gl3 = [f.gl for f in fields.values() if f.tag == 3]
    gb3 = [f.gb for f in fields.values() if f.tag == 3]
    n3 = len(ra3)

    if equfile != "" :
        equf = moll(lat_range=(-5,88))
        equf.grid(lat_lab_lon=0, lon_lab_lat=-5, lat_step=10)
        equf.scatter(ra0, de0, "k,", label="Future {}".format(n0))
        equf.scatter(ra1, de1, "bs", label="Done {}".format(n1+n3))
        if marktext is not None :
            equf.scatter(ra3, de3, "rs", label="{} {}".format(marktext, n3))
        plt.legend()
        plt.title("{tel} Footprint in Equatorial System".format(tel=tel))
        plt.savefig(equfile)
        plt.close()

    if galfile != "" :
        galf = moll()
        galf.grid(lat_lab_lon=0, lon_lab_lat=-5)
        galf.scatter(gl0, gb0, "k,", label="Future {}".format(n0))
        galf.scatter(gl1, gb1, "bs", label="Done {}".format(n1+n3))
        if marktext is not None :
            galf.scatter(gl3, gb3, "rs", label="{} {}".format(marktext, n3))
        plt.legend()
        plt.title("{tel} Footprint in Galactic System".format(tel=tel))
        plt.savefig(galfile)
        plt.close()


if __name__ =="__main__" :
    import args

    ar = {"tel":None, "text":None, "equ":None, "gal":None, "run":None, "day":None, "before":False}
    al = {"arg_01" : "tel"}
    ar = args.arg_trans(sys.argv, ar, silent=True, alias=al)

    if ar["tel"] is None :
        print ("""Syntax:
    python footprint.py tel [text=textfile] [equ=equfile] [gal=galfile] [run=run] [day=day] [before=]
        tel: 3 letter code of telescope, we now have bok and xao
        textfile: output text report file
        equfile: output file name for Equatorial System
        galfile: output file name for Galactic System
        run: code of run, usually as yyyymm format
        day: modified Julian day of the date, 4 digit, JD-2450000.5
        before: draw covered before specified run or day, nothing after "="
    """)
    else :
        footprint(ar["tel"], run=ar["run"], day=ar["day"], before=ar["before"],
                  reportfile=ar["text"], equfile=ar["equ"], galfile=ar["gal"])