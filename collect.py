"""
    Module collect : part of SAGE Digital Sky Survey Observation Scheduler
    v 1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    This function collect file info, and generate obsed list
"""


import os
import time
import util
import schdutil


def collect ( tel, runcode ) :
    """
    """
    # search check filenames
    obsedpath = "{tel}/obsed/{runcode}/".format(tel=tel, runcode=runcode)
    if not os.path.isdir(obsedpath) :
        print ("ERROR: `{}` does NOT exists".format(obsedpath))
    chkfiles = [obsedpath + f
                for f in os.listdir(obsedpath)
                if f.startswith("check.J") and f.endswith(".lst") and os.path.isfile(obsedpath+f)]

    # load configure file
    plans = schdutil.load_expplan(tel)
    modes = schdutil.load_expmode(tel)

    # load check files
    chk = []
    for cf in chkfiles :
        lines = open(cf, "r").readlines()
        for line in lines :
            c = schdutil.check_info.parse(line)
            #pp = line.split() #filesn imagetype object filter exptime ra dec filename
            #c = {"filesn":int(pp[0]), "imagetype":pp[1], "object":pp[2],
            #     "filter":pp[3], "expt":float(pp[4]),
            #     "ra":float(pp[5]), "dec":float(pp[6]), "filename":pp[7]}
            # check mode, code, and factor
            mode = c.mode()
            c.mode = mode
            if mode in modes :
                c.code = modes[mode].code
                c.factor = modes[mode].factor
            else :
                c.code = -1
                c.factor = 0.0
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
    obsedlst = obsedpath + "obsed.lst"
    if os.path.isfile(obsedlst) :
        obsedbak = obsedpath + "obsed." + time.strftime("%Y%m%d%H%M%S") + ".bak"
        os.rename(obsedlst, obsedbak)
        print ("Current list backup to `{}`".format(obsedbak))

    f = open(obsedlst, "w")
    f.write("# Generated at {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S")))
    f.write("#{:<11s}".format("Object"))
    for p in plans :
        f.write(" {:>4s}".format(plans[p].name[0:4]))
    f.write("\n\n")
    for o in objmap :
        ot = "{:<12s}".format(o)
        ft = ["{:>4.1f}".format(objmap[o][c]) for c in objmap[o] if c >= 0]
        tt = ot + " " + " ".join(ft) + "\n"
        f.write(tt)
    f.close()

    print ("Successfully collect {1} objects from {0} files of run `{2}-{3}`.".format(
        len(chkfiles), len(objmap), tel, runcode))

if __name__ =="__main__" :
    collect("bok","201603B")
