# -*- coding: utf-8 -*-
"""
    Module schdutil
    Special utilities for Scheduler
    v1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

"""

import os
import numpy as np
import common


class base_info (object) :
    """ Base for structure like class, holding fields
    """
    def __init__ (self, **kwargs) :
        self.__dict__ = kwargs


class plan_info (base_info) :
    """ A structure like class, holding info of plan
    """
    def __init__ (self, code, name, filter, expt, repeat, factor, active, dither1, dither2) :
        base_info.__init__(self,
            code=code, name=name, filter=filter, expt=expt, repeat=repeat, factor=factor,
            active=active, dither1=dither1, dither2=dither2)

    @staticmethod
    def parse (line) :
        """ Parse a new instance from line, columns seperated by space
        Col: code, name, filter, expt, repeat, factor, active, dither1, dither2
        dither1/2 are optional, default 0.0 0.0
        """
        xline = line + " 1 0.0 0.0" # add extra fields, add up the missing fields
        pp = xline.split()
        x = plan_info(int(pp[0]), pp[1], pp[2], float(pp[3]),
                      int(pp[4]), float(pp[5]), (int(pp[6]) != 0), float(pp[7]), float(pp[8]))
        return x

    def __repr__ (self) :
        return ("{s.code:<2d} {s.name:>10s} {s.filter:>8s} {s.expt:>5.1f} {s.repeat:>2d} {s.factor:>3.1f} "
                "{s.active:1d} {s.dither1:>5.1f} {s.dither2:>5.1f}").format(s=self)


class mode_info (base_info) :
    """ A structure like class, holding info of mode
    """
    def __init__ (self, filter, expt, code, factor) :
        base_info.__init__(self,
            filter=filter, expt=expt, code=code, factor=factor)

    @staticmethod
    def parse (line) :
        """ Parse a new instance from line, columns seperated by space
        Col: filter, expt, code, factor
        """
        pp = line.split()
        x = mode_info(pp[0], float(pp[1]), int(pp[2]), float(pp[3]))
        return x

    def mode (self) :
        """ Return the mode id string, consists of filter and expt
        """
        return "{m.filter}_{m.expt:05.1f}".format(m=self)

    def __repr__ (self) :
        return "{s.filter:<8s} {s.expt:>5.1f} {s.code:>2d} {s.factor:>3.1f}".format(s=self)


class check_info (base_info) :
    """ A structure like class, holding info of check
    """
    def __init__ (self, fitsfile, filesn, imgtyp, object, filter, expt, ra, de) :
        base_info.__init__(self,
            fitsfile=fitsfile, filesn=filesn,
            imgtyp=imgtyp, object=object, filter=filter, expt=expt,
            ra=ra, de=de)

    @staticmethod
    def parse (line) :
        """ Parse a new instance from line, columns seperated by space
        Col: filesn, imgtyp, object, filter, expt, ra, de, fitsfile
        NOTE: different to init, fitefilename is the last in text
        """
        pp = line.split()
        x = check_info(pp[7], int(pp[0]), pp[1], pp[2],
                       pp[3], float(pp[4]), float(pp[5]), float(pp[6]))
        return x

    @staticmethod
    def simulate(plan, field) :
        """ Simulate a exposure check info from expplan and field
        """
        x = check_info("SIMULATED.fits", 0, "OBJECT",
                       str(field.id), plan.filter, plan.expt, field.ra, field.de)
        return x

    def mode (self) :
        """ Return the mode id string, consists of filter and expt
        """
        return "{m.filter}_{m.expt:05.1f}".format(m=self)

    def __repr__ (self) :
        return ("{s.filesn:04d} {s.imgtyp:>8s} {s.object:>10s} {s.filter:>8s} {s.expt:>5.1f} "
                "{s.ra:>9.5f} {s.de:>+9.5f} {s.fitsfile}").format(s=self)


class field_info (base_info) :
    """ A structure like class, holding info of field
    """
    def __init__ (self, id, ra, de, gl, gb, bk) :
        base_info.__init__(self,
            id=id, gl=gl, gb=gb, ra=ra, de=de, bk=bk)

    @staticmethod
    def parse (line) :
        """ Parse a new instance from line, columns seperated by space
        Col: id, ra, dec, gl, gb, block name
        """
        pp = line.split()
        x = field_info(int(pp[0]), float(pp[1]), float(pp[2]), float(pp[3]), float(pp[4]), pp[5])
        return x

    def __repr__ (self) :
        fmt = "{s.id:<5d}  {s.ra:>9.5f} {s.de:>+9.5f}  {s.gl:>9.5f} {s.gb:>+9.5f}  {s.bk:s}"
        #if self.__dict__.has_key("tag") :
        if "tag" in self.__dict__ :
            fmt += "  {s.tag:1d}"
        return fmt.format(s=self)

    def airmass (self, lat, lst) :
        return common.sky.airmass(lat, lst, self.ra, self.de)

    def azalt (self, lat, lst) :
        return common.sky.azalt(lat, lst, self.ra, self.de)


class block_info (base_info) :
    """ A structure like class, holding info of block
    """
    def __init__ (self, bname, fields) :
        ix = np.argsort([f.ra for f in fields])
        base_info.__init__(self,
            bname=bname, fields=fields[ix],
            ra=np.mean([f.ra for f in fields]), de=np.mean([f.de for f in fields]) )

    def __repr__ (self) :
        return "{bn}: {ra:11} {de:11} {fn:>2}# [{f}]".format(
            bn=self.bname, ra=common.angle.dec2hms(self.ra), de=common.angle.dec2dms(self.dec), fn=len(self.fields),
            f=",".join(["{:>5d}".format(f.id) for f in self.fields]) )


class exposure_info (base_info) :
    """ holding exposure info, and get different format of output
    """
    def __init__ (self, obj, filter, expt, ra, de) :
        base_info.__init__(self,
            obj=obj, filter=filter, expt=expt, ra=ra, de=de)

    @staticmethod
    def make (plan, field) :
        """ make a exposure with plan and field
        """
        return exposure_info(field.id, plan.filter, plan.expt, field.ra, field.de)

    # some propperties, providing more formats for output
    @property
    def objs (self)  : return str(self.obj)
    @property
    def expti (self) : return int(self.expt)
    @property
    def exptf (self) : return self.expt
    @property
    def rad (self) :   return self.ra
    @property
    def ded (self) :   return self.de
    @property
    def ras (self) :   return common.angle.dec2hms(self.ra)
    @property
    def des (self) :   return common.angle.dec2dms(self.de)
    @property
    def rap (self) :   return common.angle.dec2hms(self.ra, len=9, delimiter="")
    @property
    def dep (self) :   return common.angle.dec2dms(self.de, len=9, delimiter="")


####################################################################################################


def load_basic (tel) :
    """ Load basic info of site and telescope
    args:
        tel: telescope brief code
    returns:
        object of site basic data
        keys: lon, lat, alt, tz, interval, fov, lons, lats, bmove, fmt
    """
    basicfile = "{tel}/conf/basic.txt".format(tel=tel)
    basiclines = common.util.read_conf(basicfile, default=[])
    nb = len(basiclines)

    basic = base_info(lon=-111.6, lat=+31.96, alt=2096.0, tz=-7, lons="-111:35:48", lats="31:57:30",
                      inter=50.0, fov=0.9, bmove = 90.0,
                      fmt="obs   {e.expt:5.1f}  object     {e.obj:>8}  1  {e.filter:>8}  {e.rap:9}  {e.dep:9}  2000.0")
    if nb >= 1 : basic.lon   = common.angle.dms2dec(basiclines[0]) ; basic.lons = basiclines[0]
    if nb >= 2 : basic.lat   = common.angle.dms2dec(basiclines[1]) ; basic.lats = basiclines[1]
    if nb >= 3 : basic.alt   = float(basiclines[2])
    if nb >= 4 : basic.tz    = float(basiclines[3])
    if nb >= 5 : basic.inter = float(basiclines[4])
    if nb >= 6 : basic.fov   = float(basiclines[5])
    if nb >= 7 : basic.bmove = float(basiclines[6])
    if nb >= 8 : basic.fmt   = basiclines[7]

    return basic


def load_expplan (tel) :
    """ Load exposure plan from conf file
    args:
        tel: telescope brief code
    returns:
        dict of plans, key is plancode, value is a plan
        a plan is a instance of class plan_info
        plan is configure for future observation, may be difference with old obs
    """
    expplanfile = "{tel}/conf/expplan.txt".format(tel=tel)
    planlines = common.util.read_conf(expplanfile, default=["0 u60 u 60 1 1 0 0"])

    plans = {}
    for line in planlines :
        a = plan_info.parse(line)
        plans[a.code] = a

    return plans


def load_expmode (tel) :
    """ Load exposure mode from conf file
    args:
        tel: telescope brief code
    returns:
        dict of modes, key is mode code, value is a exposure mode
        mode code consists of filter and expt
        a mode is a instance of class mode_info
        mode is a connection between real exposure mode and plan
    """
    expmodefile = "{tel}/conf/expmode.txt".format(tel=tel)
    modelines = common.util.read_conf(expmodefile, default=["u 60 0 1"])

    modes = {}
    for line in modelines :
        a = mode_info.parse(line)
        modes[a.mode()] = a

    return modes


def load_field (tel) :
    """ Load field definition from conf file
    args:
        tel: telescope brief code
    returns:
        dict of fields, key is field id, value is a field
        a field is a instance of class field_info
    """
    fieldfile = "{tel}/conf/field.txt".format(tel=tel)
    fieldlines = common.util.read_conf(fieldfile, default=None)

    fields = {}
    for line in fieldlines :
        a = field_info.parse(line)
        fields[a.id] = a

    return fields


def load_obsed (fields, obsedlist, plans, marklist=None) :
    """ load obsed list, and sum obsed factor to fields.
    args:
        fields: input and output, field dict, each object will add factor, mark, and tag
        obsedlist: obsed file to be loaded
        plans: plan dict
        marklist: mark file, factor in this list will be sum to mark array
        x/plancode: sorted plan code, only code, not whole plan
        x/plan: if specified, use this plan to judge tag, else any plan
    returns:
        Nothing. Obsed factor and tag updated in fields
    """
    plancode = plans.keys()
    plancode.sort()
    nplan = len(plans)
    if marklist is None : marklist = []
    # add empty factor for all field
    emptyfactor = {} # make an empty factor
    for p in plancode :
        emptyfactor[p] = 0.0
    for f in fields :
        fields[f].factor = emptyfactor.copy()
        fields[f].mark = emptyfactor.copy()

    # load obsed list and mark fields
    for obsed in obsedlist :
        factorlines = open(obsed, "r").readlines()
        ismarked = obsed in marklist
        for factor in factorlines[2:] : # skip 2 heading line
            pp = factor.strip().split()
            if pp[0].isdigit() : # handle only survey field, int, discard other test
                id = int(pp[0])
                if id in fields :
                    for i in range(nplan) :
                        fields[id].factor[plancode[i]] += float(pp[i+1])
                        if ismarked :
                            fields[id].mark[plancode[i]] += float(pp[i+1])

    # get tag: mark <= fmax, fmin <= fmax, mark <=> fmin
    #    0 unobserved               -- fmax == 0 ==> fmin=0,mark=0
    #    1 partly observed unmarked -- fmin <  1
    #    2 full observed unmarked   -- fmin >= 1
    #    3 marked                   -- mark > 0

    # old version using plan
    #if plan is None :
    #    for f in fields :
    #        fmax = max(fields[f].factor.values())
    #        fmin = min(fields[f].factor.values())
    #        mark = max(fields[f].mark.values())
    #        fields[f].tag = 0 if fmax == 0.0 else \
    #                        3 if mark >  0.0 else \
    #                        1 if fmin <  1.0 else 2
    #else :
    #    for f in fields :
    #        fmin = fmax = fields[f].factor[plan]
    #        mark = fields[f].mark[plan]
    #        fields[f].tag = 0 if fmax == 0.0 else \
    #                        3 if mark >  0.0 else \
    #                        1 if fmin <  1.0 else 2

    # new version using plans.active
    for f in fields.values() :
        activefactor = [f.factor[p] for p in plancode if plans[p].active]
        activemark = [f.mark[p] for p in plancode if plans[p].active]
        fmax = max(activefactor)
        fmin = min(activefactor)
        mark = max(activemark)
        f.tag = (0 if fmax == 0.0 else
                 3 if mark > 0.0 else
                 1 if fmin < 1.0 else
                 2)


def ls_files (wildcard) :
    """ Execute a ls command with wildcard, and return file list
    args:
        wildcard: target of ls command
    returns:
        list of found files
    """
    return [f.strip() for f in os.popen("ls " + wildcard).readlines()]
