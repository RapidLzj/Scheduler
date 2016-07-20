"""
    Module footprint : part of SAGE Digital Sky Survey Observation Scheduler
    v 1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    This function draw footprint of specified run, day and plan
"""


import os
import sys
import time
from myPyLib.Mollweide import moll
from matplotlib import pyplot as plt
import util
import schdutil


def footprint ( tel, reportfile=None, equfile=None, galfile=None,
                run=None, day=None, plan=None, before=False ) :
    """ Draw footprint
    """
    # set default output file
    dt = time.strftime("%Y%m%d%H%M%S")
    if reportfile == None :
        reportfile = "{tel}/obsed/footprint/report.{dt}.txt".format(tel=tel, dt=dt)
    if equfile == None :
        equfile = "{tel}/obsed/footprint/equ.{dt}.png".format(tel=tel, dt=dt)
    if galfile == None :
        galfile = "{tel}/obsed/footprint/gal.{dt}.png".format(tel=tel, dt=dt)

    # load fields configure file
    plans  = schdutil.load_expplan(tel)
    fields = schdutil.load_field(tel)
    plancode = plans.keys()
    plancode.sort()
    np = len(plancode)
    if plan != None and plan not in plancode :
        plan = None
    if plan != None :
        planname = plans[plan].name
    else :
        planname = ""

    # find all obsed file
    obsedlist = schdutil.ls_files("{tel}/obsed/*/obsed.J*.lst".format(tel=tel))

    if run != None and day != None :
        marklist = schdutil.ls_files("{tel}/obsed/{run}/obsed.J{day:0>4d}.lst".format(tel=tel, run=run, day=day))
        marktext = "J{day:0>4d}".format(run=run, day=day)
    elif run != None and day == None :
        marklist = schdutil.ls_files("{tel}/obsed/{run}/obsed.J*.lst".format(tel=tel, run=run))
        marktext = "{run}".format(run=run, day=day)
    else :
        marklist = []
        marktext = None

    if before :
        maxmark = max(marklist)
        obsedlist = [f for f in obsedlist if f <= maxmark]

    # add empty factor for all field
    emptyfactor = {} # make an empty factor
    for p in plancode :
        emptyfactor[p] = 0.0
    for f in fields :
        fields[f].factor = emptyfactor.copy()
        fields[f].mark = emptyfactor.copy()

    # mark fields
    for obsed in obsedlist :
        factorlines = open(obsed, "r").readlines()
        ismark = obsed in marklist
        for factor in factorlines[2:] : # skip 2 heading line
            pp = factor.strip().split()
            if pp[0].isdigit() :
                id = int(pp[0])
                if id in fields :
                    for i in range(np) :
                        fields[id].factor[plancode[i]] += float(pp[i+1])
                        if ismark :
                            fields[id].mark[plancode[i]] += float(pp[i+1])

    # get tag: 0 unobserved, 1 observed unmarked, 2 marked
    if plan == None :
        for f in fields :
            fsum = sum(fields[f].factor.values())
            msum = sum(fields[f].mark.values())
            fields[f].tag = 0 if fsum == 0.0 else 1 if msum == 0.0 else 2
    else :
        for f in fields :
            fsum = fields[f].factor[plan]
            msum = fields[f].mark[plan]
            fields[f].tag = 0 if fsum == 0.0 else 1 if msum == 0.0 else 2

    # generate a text report
    rep = open(reportfile, "w")
    for f in fields.values() :
        rep.write(("{0}  {1:1d} ").format(f, f.tag))
        for p in plancode :
            rep.write(" {:>4.1f}".format(f.factor[p]))
        for p in plancode :
            rep.write(" {:>4.1f}".format(f.mark[p]))
        rep.write("\n")
    rep.close()

    # draw Equatorial System
    plt.rcParams['figure.figsize'] = 16,10

    ra0 = [f.ra for f in fields.values() if f.tag == 0]
    de0 = [f.de for f in fields.values() if f.tag == 0]
    gl0 = [f.gl for f in fields.values() if f.tag == 0]
    gb0 = [f.gb for f in fields.values() if f.tag == 0]
    n0 = len(ra0)
    ra1 = [f.ra for f in fields.values() if f.tag == 1]
    de1 = [f.de for f in fields.values() if f.tag == 1]
    gl1 = [f.gl for f in fields.values() if f.tag == 1]
    gb1 = [f.gb for f in fields.values() if f.tag == 1]
    n1 = len(ra1)
    ra2 = [f.ra for f in fields.values() if f.tag == 2]
    de2 = [f.de for f in fields.values() if f.tag == 2]
    gl2 = [f.gl for f in fields.values() if f.tag == 2]
    gb2 = [f.gb for f in fields.values() if f.tag == 2]
    n2 = len(ra2)

    equf = moll(lat_range=(-5,85))
    equf.grid(lat_lab_lon=0, lon_lab_lat=-5, lat_step=10)
    equf.scatter(ra0, de0, "k,", label="Future {}".format(n0))
    equf.scatter(ra1, de1, "b.", label="Done {}".format(n1+n2))
    if marktext != None :
        equf.scatter(ra2, de2, "r.", label="{} {}".format(marktext, n2))
    plt.legend()
    plt.title("{tel} {plan} Footprint in Equatorial System".format(tel=tel, plan=planname))
    plt.savefig(equfile)
    plt.close()


    galf = moll()
    galf.grid(lat_lab_lon=0, lon_lab_lat=-5)
    galf.scatter(gl0, gb0, "k,", label="Future {}".format(n0))
    galf.scatter(gl1, gb1, "b.", label="Done {}".format(n1+n2))
    if marktext != None :
        galf.scatter(gl2, gb2, "r.", label="{} {}".format(marktext, n2))
    plt.legend()
    plt.title("{tel} {plan} Footprint in Galactic System".format(tel=tel, plan=planname))
    plt.savefig(galfile)
    plt.close()


if __name__ =="__main__" :
    if len(sys.argv) < 2 :
        print ("""Syntax:
    python footprint.py tel [Ttextfile] [Eequfile] [Ggalfile] [Rrun] [Dday] [Pplan] [B]
        tel: 3 letter code of telescope, we now have bok and xao
        textfile: output text report file
        equfile: output file name for Equatorial System
        galfile: output file name for Galactic System
        run: code of run, usually as yyyymm format
        day: modified Julian day of the date, 4 digit, JD-2450000.5
        plan: plan code to draw
        before: draw covered bofore specified run or day
        for optional argument, need a leading capital E, G, R, D or P, B
    """)
    else :
        txtfile, equfile, galfile = None, None, None
        run, day, plan = None, None, None
        before = False
        for a in sys.argv[2:] :
            if a.startswith("R") :
                run = a[1:]
            elif a.startswith("D") :
                day = int(a[1:])
            elif a.startswith("P") :
                plan = int(a[1:])
            elif a.startswith("E") :
                equfile = a[1:]
            elif a.startswith("T") :
                txtfile = a[1:]
            elif a.startswith("G") :
                galfile = a[1:]
            elif a.startswith("B") :
                before = True
        print txtfile, equfile, galfile, run, day, plan, before
        footprint(sys.argv[1], run=run, day=day, plan=plan, before=before,
                  reportfile=txtfile, equfile=equfile, galfile=galfile)