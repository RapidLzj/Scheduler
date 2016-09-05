#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Module xao_after_obs : part of SAGE Digital Sky Survey Observation Scheduler
    v 1.0 : By Jie Zheng, 201609, Tucson, AZ, USA

    This module calls ls, check, collect, and footprint for past night
"""


import os
import common
import schdutil
from check import check
from collect import collect
from footprint import footprint


def after_obs_bok (yr, mn, dy, run=None, path=None) :
    ''' A shell calls ls, check, collect, and footprint. Only for xao
    Standard path is /home/primefocus/data/bss/yyyymmdd
    Args:
        yr: year
        mn: month
        dy: day
        run: run name, default is yyyymm
        path: optional, root path of the day
    '''
    # arguments default
    if run is None or run == "" :
        run = "{y:0>4d}{m:0>2d}".format(y=yr, m=mn, d=dy)
    if path is None or path == "" :
        path = "/home/primefocus/data/bss/{y:0>4d}{m:0>2d}{d:0>2d}".format(y=yr, m=mn, d=dy)
    # data of night
    class psite : pass
    site = psite()
    site.tz = -7
    mjd18 = common.sky.mjd_of_night(yr, mn, dy, site)
    tel = "bok"
    # files of the day
    filelist = "{tel}/obsed/{run}/files.J{day:04d}.lst".format(tel=tel, run=run, day=mjd18)
    checkfile = "{tel}/obsed/{run}/check.J{day:04d}.lst".format(tel=tel, run=run, day=mjd18)
    obsedfile = "{tel}/obsed/{run}/obsed.J{day:04d}.lst".format(tel=tel, run=run, day=mjd18)
    repfile = "{tel}/obsed/footprint/Rep_J{mjd}.txt".format(tel=tel, mjd=mjd18)
    equfile = "{tel}/obsed/footprint/Equ_J{mjd}.png".format(tel=tel, mjd=mjd18)
    galfile = "{tel}/obsed/footprint/Gal_J{mjd}.png".format(tel=tel, mjd=mjd18)
    # 1. call ls
    os.system("ls {path}/sage_survey/*/*.fits > {filelist}".format(path=path, filelist=filelist))
    # 2. call check
    check(tel, yr, mn, dy, run)
    # 3. call collect
    collect(tel, yr, mn, dy, run)
    # 4. call footprint
    footprint(tel, reportfile=repfile, equfile=equfile, galfile=galfile, run=run, day=mjd18)
    # info
    print ("Send following files to SAGE Survey group:"
           "\t{filelist}"
           "\t{checkfile}"
           "\t{obsedfile}"
           "\t{equfile}"
           "\t{galfile}"
           "\t{repfile}".format(
        filelist=filelist, checkfile=checkfile, obsedfile=obsedfile,
        equfile=equfile, galfile=galfile, repfile=repfile
    ))


if __name__ == "__main__" :
    import sys
    import args

    ar = {"year":sys.maxsize, "month":sys.maxsize, "day":sys.maxsize,
          "run":"", "path":""}
    al = {"arg_01":"tel", "arg_02":"year", "arg_03":"month", "arg_04":"day",
          "arg_05":"run", "arg_06":"path"}
    ar = args.arg_trans(sys.argv, ar, silent=True, alias=al)

    if ar["day"] == sys.maxsize :
        print("""Syntax:
    ./xao_after_obs.py year month day [run [path]]
        year: 4-digit year
        month: month number, 1 to 12
        day: day number, 1 to 31, or extended
        run: code of run, usually as yyyymm format
        path: root path of the day
    """)
    else :
        after_obs_bok(ar["year"], ar["month"], ar["day"], ar["run"], ar["path"])
