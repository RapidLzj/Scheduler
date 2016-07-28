# -*- coding: utf-8 -*-
"""
    Module schdutil
    Special utilities for Scheduler
    v1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    Providing:
        class plan_info, mode_info, check_info
        load_expplan
        load_expfactor
"""

import os
import sys
import numpy as np
import util


class base_info :
    """ Base for structure like class, holding fields
    """
    def __init__ (self, **kwargs) :
        self.__dict__ = kwargs


class plan_info (base_info) :
    """ A structure like class, holding info of plan
    """
    def __init__ (self, code, name, filter, expt, repeat, factor, dither1, dither2) :
        base_info.__init__(self,
            code=code, name=name, filter=filter, expt=expt, repeat=repeat, factor=factor,
            dither1=dither1, dither2=dither2)

    @staticmethod
    def parse ( line ) :
        """ Parse a new instance from line, columns seperated by space
        Col: code, name, filter, expt, repeat, factor, dither1, dither2
        dither1/2 are optional, default 0.0 0.0
        """
        xline = line + " 0.0 0.0" # add extra fields, add up the missing fields
        pp = xline.split()
        x = plan_info(int(pp[0]), pp[1], pp[2], float(pp[3]),
                      int(pp[4]), float(pp[5]), float(pp[6]), float(pp[7]))
        return x

    def __repr__ ( self ) :
        return ("{s.code:<2d} {s.name:>10s} {s.filter:>8s} {s.expt:>5.1f} " +
                "{s.repeat:>2d} {s.factor:>3.1f} {s.dither1:>5.1f} {s.dither2:>5.1f}").format(s=self)


class mode_info (base_info) :
    """ A structure like class, holding info of mode
    """
    def __init__ ( self, filter, expt, code, factor ) :
        base_info.__init__(self,
            filter=filter, expt=expt, code=code, factor=factor)

    @staticmethod
    def parse ( line ) :
        """ Parse a new instance from line, columns seperated by space
        Col: filter, expt, code, factor
        """
        pp = line.split()
        x = mode_info(pp[0], float(pp[1]), int(pp[2]), float(pp[3]))
        return x

    def mode ( self ) :
        """ Return the mode id string, consists of filter and expt
        """
        return "{m.filter}_{m.expt:05.1f}".format(m=self)

    def __repr__ ( self ) :
        return "{s.filter:<8s} {s.expt:>5.1f} {s.code:>2d} {s.factor:>3.1f}".format(s=self)


class check_info (base_info) :
    """ A structure like class, holding info of check
    """
    def __init__ ( self, fitsfile, filesn, imgtyp, object, filter, expt, ra, de ) :
        base_info.__init__(self,
            fitsfile=fitsfile, filesn=filesn,
            imgtyp=imgtyp, object=object, filter=filter, expt=expt,
            ra=ra, de=de)

    @staticmethod
    def parse ( line ) :
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

    def mode ( self ) :
        """ Return the mode id string, consists of filter and expt
        """
        return "{m.filter}_{m.expt:05.1f}".format(m=self)

    def __repr__ ( self ) :
        return ("{s.filesn:04d} {s.imgtyp:>8s} {s.object:>10s} {s.filter:>8s} {s.expt:>5.1f} "
                "{s.ra:>9.5f} {s.de:>+9.5f} {s.fitsfile}").format(s=self)


class field_info (base_info) :
    """ A structure like class, holding info of field
    """
    def __init__ ( self, id, ra, de, gl, gb, bk ) :
        base_info.__init__(self,
            id = id, gl = gl, gb = gb, ra = ra, de = de, bk = bk)

    @staticmethod
    def parse ( line ) :
        """ Parse a new instance from line, columns seperated by space
        Col: id, ra, dec, gl, gb, block name
        """
        pp = line.split()
        x = field_info(int(pp[0]), float(pp[1]), float(pp[2]), float(pp[3]), float(pp[4]), pp[5])
        return x

    def __repr__ ( self ) :
        fmt = "{s.id:<5d}  {s.ra:>9.5f} {s.de:>+9.5f}  {s.gl:>9.5f} {s.gb:>+9.5f}  {s.bk:s}"
        if self.__dict__.has_key("tag") : fmt += "  {s.tag:1d}"
        return fmt.format(s=self)


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
            bn=self.bname, ra=util.dec2hms(self.ra), de=util.dec2dms(self.dec), fn=len(fields),
            f=",".join(["{:>5d}".format(f.id) for f in fields]) )


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
    def objs (self)  : return str(obj)
    @property
    def expti (self) : return int(self.expt)
    @property
    def exptf (self) : return self.expt
    @property
    def rad (self) :   return ra
    @property
    def ded (self) :   return de
    @property
    def ras (self) :   return util.dec2hms(self.ra)
    @property
    def des (self) :   return util.dec2dms(self.de)
    @property
    def rap (self) :   return util.dec2hms(self.ra, len=9, delimiter="")
    @property
    def dep (self) :   return util.dec2dms(self.de, len=9, delimiter="")


####################################################################################################


def load_basic ( tel ) :
    """ Load basic info of site and telescope
    args:
        tel: telescope brief code
    returns:
        dict of site basic data
        keys: lon, lat, alt, tz, interval, fov, lons, lats
    """
    basicfile = "{tel}/conf/basic.txt".format(tel=tel)
    basiclines = util.read_conf(basicfile, default=[])
    nb = len(basiclines)

    basic = base_info(lon=-111.6, lat=+31.96, alt=2096.0, tz=-7, lons="-111:35:48", lats="31:57:30",
                      inter=50.0, fov=0.9,
                      fmt="obs   {e.expt:5.1f}  object     {e.obj:>8}  1  {e.filter:>8}  {e.rap:9}  {e.dep:9}  2000.0")
    if nb >= 1 : basic.lon   = util.dms2dec(basiclines[0]) ; basic.lons = basiclines[0]
    if nb >= 2 : basic.lat   = util.dms2dec(basiclines[1]) ; basic.lats = basiclines[1]
    if nb >= 3 : basic.alt   =        float(basiclines[2])
    if nb >= 4 : basic.tz    =        float(basiclines[3])
    if nb >= 5 : basic.inter =        float(basiclines[4])
    if nb >= 6 : basic.fov   =        float(basiclines[5])
    if nb >= 7 : basic.fmt   =              basiclines[6]

    return basic


def load_expplan ( tel ) :
    """ Load exposure plan from conf file
    args:
        tel: telescope brief code
    returns:
        dict of plans, key is plancode, value is a plan
        a plan is a instance of class plan_info
        plan is configure for future observation, may be difference with old obs
    """
    expplanfile = "{tel}/conf/expplan.txt".format(tel=tel)
    planlines = util.read_conf(expplanfile, default=["0 u60 u 60 1 1 0 0"])

    plans = {}
    for line in planlines :
        a = plan_info.parse(line)
        plans[a.code] = a

    return plans


def load_expmode ( tel ) :
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
    modelines = util.read_conf(expmodefile, default=["u 60 0 1"])

    modes = {}
    for line in modelines :
        a = mode_info.parse(line)
        modes[a.mode()] = a

    return modes


def load_field ( tel ) :
    """ Load field definition from conf file
    args:
        tel: telescope brief code
    returns:
        dict of fields, key is field id, value is a field
        a field is a instance of class field_info
    """
    expmodefile = "{tel}/conf/field.txt".format(tel=tel)
    fieldlines = util.read_conf(expmodefile, default=None)

    fields = {}
    for line in fieldlines :
        a = field_info.parse(line)
        fields[a.id] = a

    return fields


def load_obsed ( fields, obsedlist, marklist, plancode, plan=None ) :
    """ load obsed list, and sum obsed factor to fields.
    args:
        fields: input and output, field dict, each object will add factor, mark, and tag
        obsedlist: obsed file to be loaded
        marklist: mark file, factor in this list will be sum to mark array
        plancode: sorted plan code, only code, not whole plan
        plan: if specified, use this plan to judge tag, else any plan
    """
    # add empty factor for all field
    emptyfactor = {} # make an empty factor
    for p in plancode :
        emptyfactor[p] = 0.0
    for f in fields :
        fields[f].factor = emptyfactor.copy()
        fields[f].mark = emptyfactor.copy()

    # load obsed list and mark fields
    nplan = len(plancode)
    for obsed in obsedlist :
        factorlines = open(obsed, "r").readlines()
        ismark = obsed in marklist
        for factor in factorlines[2:] : # skip 2 heading line
            pp = factor.strip().split()
            if pp[0].isdigit() :
                id = int(pp[0])
                if id in fields :
                    for i in range(nplan) :
                        fields[id].factor[plancode[i]] += float(pp[i+1])
                        if ismark :
                            fields[id].mark[plancode[i]] += float(pp[i+1])

    # get tag: mark <= fmax, fmin <= fmax, mark <=> fmin
    #    0 unobserved               -- fmax == 0 ==> fmin=0,mark=0
    #    1 partly observed unmarked -- fmin <  1
    #    2 full observed unmarked   -- fmin >= 1
    #    3 marked                   -- mark > 0
    if plan is None :
        for f in fields :
            fmax = max(fields[f].factor.values())
            fmin = min(fields[f].factor.values())
            mark = max(fields[f].mark.values())
            fields[f].tag = 0 if fmax == 0.0 else \
                            3 if mark >  0.0 else \
                            1 if fmin <  1.0 else 2
    else :
        for f in fields :
            fmin = fmax = fields[f].factor[plan]
            mark = fields[f].mark[plan]
            fields[f].tag = 0 if fmax == 0.0 else \
                            3 if mark >  0.0 else \
                            1 if fmin <  1.0 else 2


def ls_files ( wildcard ) :
    """ Execute a ls command with wildcard, and return file list
    args:
        wildcard: target of ls command
    returns:
        list of found files
    """
    return [f.strip() for f in os.popen("ls " + wildcard).readlines()]


def day_of_year (yr, mn, dy) :
    """ day serial number in year, Jan 01 as 1
    args:
        yr: year, 2 or 4 digit year
        mn: month, 1 to 12
        dy: day, 1 to 31, extended days also acceptable
    returns:
        day number in the year
    """
    md = [0,  31, 28, 31,  30, 31, 30,  31, 31, 30,  31, 30, 31] # days in month
    dofy = sum(md[1:mn]) + dy  # day of year
    if yr % 4 == 0 and mn > 2 : dofy += 1 # leap year
    return dofy


def fmst (yr, mn, dy, lon) :
    """ Fast Midnight Sidereal Time Calculation, precious about 1 min
    args:
        yr: year, 2 or 4 digit year
        mn: month, 1 to 12
        dy: day, 1 to 31, extended days also acceptable
        lon: longitude of site, in degree, if 180 to 360 provided, will transfer to -180 to 0
    returns:
        sidereal time of midnight, in degree
    """
    base = (6 + 40 / 60.0) * 15.0 # midnight sidereal time of 12-31 of last year (day 0)
    # in fact, mid night is the new year 00:00
    doy = day_of_year(yr, mn, dy)
    yrcorr = (-yr % 4) / 60.0 * 15.0 # year correction for every 4 year
    tz = lon / 15.0
    if tz > 12.0 : tz -= 24.0
    st = (base + yrcorr + (doy - tz / 24) / 365.25 * 360.0) % 360.0 / 15.0
    return st


def mjd (yr, mn, dy, hr=0, mi=0, se=0, tz=0) :
    """ Modified Julian Day calculation
    args:
        yr: year, 4 digit year, must be int, must >= 2000
        mn: month, 1 to 12, must be int
        dy: day, 1 to 31, extended days also acceptable, int or float
        hr: hour, 0 to 23
        mi: minute, 0 to 59
        se: second, 0 to 59
        tz: timezone, -12 to 12
        extented: for dy, hr, mi, se, extended value acceptable, that means float number or
                  number out of range is also OK, and have their real means
    returns:
        modified julian day
    """
    # emjd0 = (1995, 10, 10, 0, 0, 0) # jd 2450000.5
    mjd2000 = 51544   # mjd of 2000-01-01T00:00:00.0
    yrpass = yr - 2000
    doy = day_of_year(yr, mn, dy)
    hrx = (hr - tz + mi / 60.0 + se / 3600.0) / 24.0 # time in a day
    dayall = yrpass * 365 + int((yrpass-1) / 4 + 1) + doy - 1 # days from 2000-01-01
    dd = mjd2000 + dayall + hrx
    return dd


def night_len (mjd, lat) :
    """ Fast night length of given mjd, algorithms from web
    args:
        mjd: mjd of midnight, do not care timezone and longitude
        lat: latitude of site, -90.0 to +90.0
    returns:
        night length in hours, not very accurate
    """
    SummerSolstice2015 = 57194.69236
    # day angle from Summer Solstice
    dangle = (mjd - SummerSolstice2015) / 365.244 * 2.0 * np.pi
    # sun dec: This is my approximate algorithms, assume the sunlit point goes a sin curve
    sdec = np.radians(23.5) * np.cos(dangle)
    # night length approximate algorithms
    n_l = np.arccos(np.tan(np.radians(lat)) * np.tan(sdec)) / np.pi * 24.0
    return n_l


def night_time (yr, mn, dy, lon, lat, tz) :
    """ Fast get night time of the day, sunset and sunrise time
        Use simplified sun position and time algorithms.
    args:
        yr: year, 4 digit year, must be int, must >= 2000
        mn: month, 1 to 12, must be int
        dy: day, 1 to 31, extended days also acceptable, int or float
        lon: longitude of site, in degree, if 180 to 360 provided, will transfer to -180 to 0
        lat: latitude of site, in degree, -90 to +90
        tz: timezone, -12 to 24, but 12 to 24 will transfer to -12 to 0
    returns:
        tuple of sunset and sunrise time, in hours, use 12-36 hour system
    """
    lon = lon if lon < 180.0 else lon - 360.0
    tz = tz if tz <= 12.0 else tz - 24.0
    mjd0 = mjd(yr, mn, dy, 24 - lon / 15.0)  # midnight mjd
    tzcorr = (tz - lon / 15.0) # correction for local time and timezone center time
    nl = night_len (mjd0, lat)
    sunset = 24.0 - nl / 2 + tzcorr
    sunrise = 24.0 + nl / 2 + tzcorr

    return sunset, sunrise


def airmass (lat, lst, ra, dec) :
    """ Calculate airmass
        Use simplified formular from old obs4, unknown source
    args:
        lat: latitude of site, in degrees
        lst: local sidereal time, in hours
        ra: ra of target, in degrees, scrlar or ndarray
        dec: dec of target, same shape as ra
    returns:
        airmass, same shape as ra/dec
    """
    lat = np.deg2rad(lat)
    lst = np.deg2rad(lst * 15.0)
    ra  = np.deg2rad(ra)
    dec = np.deg2rad(dec)

    x1 = np.sin(lat) * np.sin(dec)
    x2 = np.cos(lat) * np.cos(dec)
    ha = lst - ra
    x = 1.0 / (x1 + x2 * np.cos(ha))
    x[np.where((x < 0.0) | (x > 9.9))] = 9.9

    return x

