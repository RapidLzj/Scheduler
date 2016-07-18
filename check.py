"""
    Module check : part of SAGE Digital Sky Survey Observation Scheduler
    v 1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    This function check observation info from file list, and put to check list.
"""


import os
#import numpy as np
#from astropy.io import fits
#import util
import headerinfo


def check ( filelist, checklist ) :
    if not os.path.isfile(filelist) :
        print ("List file NOT exists: \'{0}\'".format(filelist))
        return

    flst = open(filelist, "r").readlines()
    clst = []
    for f in flst :
        info = headerinfo.headerinfo(f.strip())
        if info != None :
            clst.append(info)

    chkfmt = ("{filesn:0>4d} {imagetype:8s} {object:10s} {filter:8s} {exptime:>5.1f} " +
              "{ra:>9.5f} {dec:>+9.5f} {filename}\n").format
    f = open(checklist, "w")
    for c in clst :
        f.write(chkfmt(c))
        print ("{filename}".format(c))
    f.close()

    print ("Successfully check {0} files from \'{1}\'.".format(len(clst), filelist))


if __name__ =="__main__" :
    pass
