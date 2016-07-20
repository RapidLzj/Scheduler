"""
    Module check : part of SAGE Digital Sky Survey Observation Scheduler
    v 1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    This function check observation info from file list, and put to check list.
"""


import os
import sys
import util
import headerinfo


def check ( tel, run, day ) :
    """
    """
    # input and output filename
    filelist = "{tel}/obsed/{run}/files.J{day:0>4d}.lst".format(tel=tel, run=run, day=day)
    chklist  = "{tel}/obsed/{run}/check.J{day:0>4d}.lst".format(tel=tel, run=run, day=day)

    if not os.path.isfile(filelist) :
        print ("ERROR!! File list NOT exists: \'{0}\'".format(filelist))
        return

    # load file info
    flst = open(filelist, "r").readlines()
    clst = []
    fcnt, i = len(flst), 0
    for f in flst :
        i += 1
        util.progress_bar(i, fcnt)
        info = headerinfo.headerinfo(f.strip())
        if info != None :
            clst.append(info)
    print ("\n")

    # output check list
    f = open(chklist, "w")
    for c in clst :
        f.write("{}\n".format(c))
    f.close()

    print ("Check OK! {0} files from `{1}`.".format(len(clst), filelist))


if __name__ =="__main__" :
    argv = sys.argv
    if len(sys.argv) < 4 :
        print ("""Syntax:
    python check.py tel run day
        tel: 3 letter code of telescope, we now have bok and xao
        run: code of run, usually as yyyymm format
        day: modified Julian day of the date, 4 digit, JD-2450000.5
    """)
    else :
        check ( sys.argv[1], sys.argv[2], int(sys.argv[3]))