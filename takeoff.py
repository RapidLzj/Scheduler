#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Module takeoff : part of SAGE Digital Sky Survey Observation Scheduler
    v 1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    Most important module in this system. This is the main schedule maker.
"""


import os
import sys
import time
import util
import schdutil


def takeoff ( tel, run, day, overwrite=False ) :
    """
    """

    #1. Load all blocks and fields, and exp plan
	#2. Load finished fields
	#3. Remove finished fields, get new blocks
	#4. Calc JD and sidereal time of midnight, and moon position
	#5. Remove blocks with moon angle lt 90
	#6. Choose a best block
	#   Algorithm for choose best
	#     Get current JD and sidereal time
	#     Calc azi and alt of all blocks, remove alt gt 80
	#     Select min of dec * 0.5 + (90-alt)*0.5
	#7. Make a script for the block, and calculate time cost
	#8. Get new "current" time, if before end time, goto 4
	#9. Ending work

    # schedule dir
    daypath = "{tel}/schedule/{run}/J{day:0>4d}/".format(tel=tel, run=run, day=day)
    if os.path.isdir(daypath) :
        if not overwrite :
            print ("ERROR!! Schedule dir already exists.\n""
                   "If you want to overwrite, please set `overwrite=True`")
            return
    os.system("mkdir -p " + daypath)
    if not os.path.isdir(daypath) :
        print ("ERROR!! Can NOT make schedule dir")

    # load fields and plan
    plans  = schdutil.load_expplan(tel)
    fields = schdutil.load_field(tel)
    plancode = plans.keys()
    plancode.sort()
    np = len(plancode)

    # find all obsed file, and mark them
    obsedlist = schdutil.ls_files("{tel}/obsed/*/obsed.J*.lst".format(tel=tel))
    schdutil.load_obsed(fields, obsedlist, [], plancode, None)
    # keep only unfinished fields
    newfield = [f for f in fields.values() if f.tag < 2]



###############################################################################

if __name__ == "__main__" :
    if len(sys.argv) < 4 :
        print ("""Syntax:
    python takeoff.py tel run day
        tel: 3 letter code of telescope, we now have bok and xao
        run: code of run, usually as yyyymm format
        day: modified Julian day of the date, 4 digit, JD-2450000.5
    """)
    else :
        ov = len(sys.argv) > 4
        takeoff(sys.argv[1], sys.argv[2], sys.argv[3], ov)