"""
    Module check : part of SAGE Digital Sky Survey Observation Scheduler
    v 1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    This function check observation info from file list, and put to check list.
"""


import os
import util
import headerinfo


def check ( tel, runcode, day ) :
    """
    """
    # input and output filename
    filelist = "{tel}/obsed/{runcode}/files.J{day:0>4d}.lst".format(tel=tel, runcode=runcode, day=day)
    chklist  = "{tel}/obsed/{runcode}/check.J{day:0>4d}.lst".format(tel=tel, runcode=runcode, day=day)

    if not os.path.isfile(filelist) :
        print ("List file NOT exists: \'{0}\'".format(filelist))
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

    print ("Successfully check {0} files from `{1}`.".format(len(clst), filelist))


if __name__ =="__main__" :
    pass
