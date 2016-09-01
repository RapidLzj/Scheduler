#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Module collect : part of SAGE Digital Sky Survey Observation Scheduler
    v 1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    This function collect file info, and generate obsed list
"""


import os
import sys
import common
import schdutil


def collect ( tel, yr, mn, dy, run="" ) :
    """ collect info from check list, compare with exposure mode and plan, make obsed list
    args:
        tel: telescope brief code
        yr: year of obs date, 4-digit year
        mn: year of obs date, 1 to 12
        dy: day of obs date, 0 to 31, or extended
        run: run code, default is `yyyymm`
    """
    site = schdutil.load_basic(tel)
    mjd18 = common.sky.mjd_of_night(yr, mn, dy, site)
    if run is None or run == "" :
        run = "{year:04d}{month:02d}".format(year=yr, month=mn)
    # search check filenames
    checklist = "{tel}/obsed/{run}/check.J{day:04d}.lst".format(tel=tel, run=run, day=mjd18)
    obsedlist = "{tel}/obsed/{run}/obsed.J{day:04d}.lst".format(tel=tel, run=run, day=mjd18)

    if not os.path.isfile(checklist) :
        print ("ERROR!! Check list NOT exists: \'{0}\'".format(checklist))
        return

    # load configure file
    plans = schdutil.load_expplan(tel)
    modes = schdutil.load_expmode(tel)

    # load check files
    chk = []
    lines = open(checklist, "r").readlines()
    pb = common.progress_bar(0, value_from=0, value_to=len(lines), value_step=0.5)
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
        pb.step()

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
        pb.step()
    pb.end()

    # output obsed file
    # get an fixed order, so no random between different system
    plancode = list(plans.keys())
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

    print ("Collect OK! {0} objects from {1} files of `{2}`.\n".format(
        len(objmap), len(lines), checklist))


if __name__ == "__main__" :
    import args

    ar = {"tel":None, "year":sys.maxsize, "month":sys.maxsize, "day":sys.maxsize, "run":""}
    al = {"arg_01":"tel", "arg_02":"year", "arg_03":"month", "arg_04":"day", "arg_05":"run"}
    ar = args.arg_trans(sys.argv, ar, silent=True, alias=al)

    if ar["day"] == sys.maxsize :
        print("""Syntax:
    python collect.py tel year month day run
        tel: 3 letter code of telescope, we now have bok and xao
        year: 4-digit year
        month: month number, 1 to 12
        day: day number, 1 to 31, or extended
        run: code of run, usually as yyyymm format
    """)
    else :
        collect(ar["tel"], ar["year"], ar["month"], ar["day"], ar["run"])
