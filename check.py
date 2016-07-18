"""
    Module check : part of SAGE Digital Sky Survey Observation Scheduler
    v 1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    This function check observation info from file list, and put to check list.
"""


import os
import util
import headerinfo


def check ( filelist, checklist ) :
    if not os.path.isfile(filelist) :
        print ("List file NOT exists: \'{0}\'".format(filelist))
        return

    flst = open(filelist, "r").readlines()
    clst = []
    c, i = len(flst), 0
    for f in flst :
        i += 1
        util.progress_bar(i, c)
        info = headerinfo.headerinfo(f.strip())
        if info != None :
            clst.append(info)
    print ("\n")

    chkfmt = ("{0[filesn]:0>4d} {0[imagetype]:8s} {0[object]:10s} {0[filter]:8s} {0[exptime]:>5.1f} " +
              "{0[ra]:>9.5f} {0[dec]:>+9.5f} {0[filename]}\n").format
    f = open(checklist, "w")
    for c in clst :
        f.write(chkfmt(c))
    f.close()

    print ("Successfully check {0} files from \'{1}\'.".format(len(clst), filelist))


if __name__ =="__main__" :
    pass
