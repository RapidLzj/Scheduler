#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Module collect : part of SAGE Digital Sky Survey Observation Scheduler
    v 1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    This function collect file info, and generate obsed list
"""


import os
import sys
import time
import util
import schdutil


def collect ( tel, run, day ) :
    """ collect info from check list, compare with exposure mode and plan, make obsed list
    args:
        tel: telescope brief code
        run: run code, usually yyyymm format
        day: 4-digit mjd of the day, JD-2450000.5
    """
    # search check filenames
    checklist  = "{tel}/obsed/{run}/check.J{day:04d}.lst".format(tel=tel, run=run, day=day)
    obsedlist  = "{tel}/obsed/{run}/obsed.J{day:04d}.lst".format(tel=tel, run=run, day=day)

    if not os.path.isfile(checklist) :
        print ("ERROR!! Check list NOT exists: \'{0}\'".format(checklist))
        return

    # load configure file
    plans = schdutil.load_expplan(tel)
    modes = schdutil.load_expmode(tel)

    # load check files
    chk = []
    lines = open(checklist, "r").readlines()
    for line in lines :
        c = schdutil.check_info.parse(line)
        mode = c.mode()
        c.mode = mode
        if mode in modes :
            c.code = modes[mode].code
            c.factor = modes[mode].factor
        else :
            c.code = -1
            c.factor = 0.0
        # remove tailing "x", which means dithered
        if c.object.endswith("x") :
            c.object = c.object[0:-1]
        chk.append(c)

    # init a empty 2-d dict `objs`, keys: obj name, plan code
    # use dict to provide an array with easy index
    uobj = set([c.object for c in chk])
    emptyobj = {-1:0.0}
    for p in plans :
        emptyobj[plans[p].code] = 0.0
    objmap = {}
    for o in uobj :
        objmap[o] = emptyobj.copy()

    # fill check info into objs
    for c in chk :
        objmap[c.object][c.code] += c.factor

    # output obsed file
    # get an fixed order, so no random between different system
    plancode = plans.keys()
    plancode.sort()
    with open(obsedlist, "w") as f :
        f.write("#{:<11s}".format("Object"))
        for p in plancode :
            f.write(" {:>4s}".format(plans[p].name[0:4]))
        f.write("\n\n")
        for o in objmap :
            ot = "{:<12s}".format(o)
            ft = ["{:>4.1f}".format(objmap[o][p]) for p in plancode]
            tt = ot + " " + " ".join(ft) + "\n"
            f.write(tt)
    #f.close()

    print ("Collect OK! {0} objects from `{1}`.".format(len(objmap), checklist))


if __name__ == "__main__" :
    if len(sys.argv) < 4 :
        print ("""Syntax:
    python collect.py tel run day
        tel: 3 letter code of telescope, we now have bok and xao
        run: code of run, usually as yyyymm format
        day: modified Julian day of the date, 4 digit, JD-2450000.5
    """)
    else :
        collect ( sys.argv[1], sys.argv[2], int(sys.argv[3]))