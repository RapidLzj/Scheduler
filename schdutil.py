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
import util

class plan_info :
    """ A structure like class, holding info of plan
    """
    def __init__ ( self, code, name, filter, expt, repeat, factor, dither1, dither2 ) :
        self.code    = code
        self.name    = name
        self.filter  = filter
        self.expt    = expt
        self.repeat  = repeat
        self.factor  = factor
        self.dither1 = dither1
        self.dither2 = dither2

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

class mode_info :
    """ A structure like class, holding info of mode
    """
    def __init__ ( self, filter, expt, code, factor ) :
        self.filter = filter
        self.expt   = expt
        self.code   = code
        self.factor = factor

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
        return "{m.filter}_{m.expt:0>5.1f}".format(m=self)

    def __repr__ ( self ) :
        return "{s.filter:<8s} {s.expt:>5.1f} {s.code:>2d} {s.factor:>3.1f}".format(s=self)

class check_info :
    """ A structure like class, holding info of check
    """
    def __init__ ( self, fitsfile, filesn, imgtyp, object, filter, expt, ra, de ) :
        self.fitsfile = fitsfile
        self.filesn = filesn
        self.imgtyp = imgtyp
        self.object = object
        self.filter = filter
        self.expt   = expt
        self.ra     = ra
        self.de     = de

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

    def mode ( self ) :
        """ Return the mode id string, consists of filter and expt
        """
        return "{m.filter}_{m.expt:0>5.1f}".format(m=self)

    def __repr__ ( self ) :
        return ("{s.filesn:0>4d} {s.imgtyp:>8s} {s.object:>10s} {s.filter:>8s} {s.expt:>5.1f} " +
                "{s.ra:>9.5f} {s.de:>+9.5f} {s.fitsfile}").format(s=self)

class field_info :
    """ A structure like class, holding info of field
    """
    def __init__ ( self, id, ra, de, gl, gb ) :
        self.id = id
        self.gl = gl
        self.gb = gb
        self.ra = ra
        self.de = de

    @staticmethod
    def parse ( line ) :
        """ Parse a new instance from line, columns seperated by space
        Col: id, ra, dec, gl, gb
        """
        pp = line.split()
        x = field_info(int(pp[0]), float(pp[1]), float(pp[2]), float(pp[3]), float(pp[4]))
        return x

    def mode ( self ) :
        """ Return the mode id string, consists of filter and expt
        """
        return "{m.filter}_{m.expt:0>5.1f}".format(m=self)

    def __repr__ ( self ) :
        return ("{s.id:<5d}  {s.ra:>9.5f} {s.de:>+9.5f}  {s.gl:>9.5f} {s.gb:>+9.5f}").format(s=self)


####################################################################################################

def load_expplan ( tel ) :
    """ Load exposure plan from conf file
    return: dict of plans, key is plancode, value is a plan
    a plan is a instance of class plan_info
    plan is configure for future observation, may be difference with old obs
    """
    expplanfile = "{tel}/conf/expplan.txt".format(tel=tel)
    planlines = util.read_conf(expplanfile, default="0 u60 u 60 1 1 0 0")

    plans = {}
    for line in planlines :
        a = plan_info.parse(line)
        plans[a.code] = a

    return plans

def load_expmode ( tel ) :
    """ Load exposure mode from conf file
    return: dict of modes, key is mode code, value is a exposure mode
    mode code consists of filter and expt
    a mode is a instance of class mode_info
    mode is a connection between real exposure mode and plan
    """
    expmodefile = "{tel}/conf/expmode.txt".format(tel=tel)
    modelines = util.read_conf(expmodefile, default="u 60 0 1")

    modes = {}
    for line in modelines :
        a = mode_info.parse(line)
        modes[a.mode()] = a

    return modes

def load_field ( tel ) :
    """ Load field definition from conf file
    return: dict of fields, key is field id, value is a field
    a field is a instance of class field_info
    """
    expmodefile = "{tel}/conf/field.txt".format(tel=tel)
    fieldlines = util.read_conf(expmodefile, default=None)

    fields = {}
    for line in fieldlines :
        a = field_info.parse(line)
        fields[a.id] = a

    return fields

def ls_files ( wildcard ) :
    """ Execute a ls command with wildcard, and return file list
    """
    return [f.strip() for f in os.popen("ls " + wildcard).readlines()]