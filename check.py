#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Module check : part of SAGE Digital Sky Survey Observation Scheduler
    v 1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    This function check observation info from file list, and put to check list.
"""


import os
import sys
import common
import schdutil
import headerinfo


def check (tel, yr, mn, dy, run=None) :
    """ check fits header, and generate a check list
    args:
        tel: telescope brief code
        yr: year of obs date, 4-digit year
        mn: year of obs date, 1 to 12
        dy: day of obs date, 0 to 31, or extended
        run: run code, default is `yyyymm`
    """
    site = schdutil.load_basic(tel)
    mjd18 = common.sky.mjd_of_night(yr, mn, dy, site)
    if run is None :
        run = "{year:04d}{month:02d}".format(year=yr, month=mn)
    # input and output filename
    filelist = "{tel}/obsed/{run}/files.J{day:04d}.lst".format(tel=tel, run=run, day=mjd18)
    chklist  = "{tel}/obsed/{run}/check.J{day:04d}.lst".format(tel=tel, run=run, day=mjd18)

    if not os.path.isfile(filelist) :
        print ("ERROR!! File list NOT exists: \'{0}\'".format(filelist))
        return

    # load file info
    flst = open(filelist, "r").readlines()
    clst = []
    fcnt, i = len(flst), 0
    pb = common.progress_bar(0, value_from=0, value_to=fcnt)
    for f in flst :
        #i += 1
        #util.progress_bar(i, fcnt)
        pb.step()
        info = headerinfo.headerinfo(f.strip())
        if info is not None :
            clst.append(info)
    #print ("\n")
    pb.end()

    # output check list
    with open(chklist, "w") as f :
        for c in clst :
            f.write("{}\n".format(c))
    #f.close()

    print ("Check OK! {0} files from `{1}`.".format(len(clst), filelist))


if __name__ == "__main__" :
    import args
    ar = {"tel":"", "year":sys.maxsize, "month":sys.maxsize, "day":sys.maxsize, "run":""}
    al = {"arg_01":"tel", "arg_02":"year", "arg_03":"month", "arg_04":"day", "arg_05":"run"}
    ar = args.arg_trans(sys.argv, ar, silent=True, alias=al)

    if ar["day"] == sys.maxsize :
        print ("""Syntax:
    python check.py tel year month day run
        tel: 3 letter code of telescope, we now have bok and xao
        year: 4-digit year
        month: month number, 1 to 12
        day: day number, 1 to 31, or extended
        run: code of run, usually as yyyymm format
    """)
    else :
        check(ar["tel"], ar["year"], ar["month"], ar["day"], ar["run"])
