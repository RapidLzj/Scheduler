# -*- coding: utf-8 -*-
"""
    Module angle
    Utilities for angle processing routine, can also be used in other task
    v1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    Providing:
        super class angle, and inherited class ra, dec, lon, lat
"""


class xangle (object) :
    """ A class about an angle, hold a angle value,
        and provide some method to transfer to other format
    """
    def __init__ (self, value, format="deg", delimiter=":", dtype="deg") :
        format = format.lower()
        self._dtype = dtype.lower()
        if format == "hour" :
            self.value = value * 15.0
        elif format == "hms" :
            self.value = self.hms2dec(value, delimiter)
        elif format == "dms" :
            self.value = self.dms2dec(value, delimiter)
        else :  #default format is "deg"
            self.value = value

    @property
    def value (self) :
        return self._value

    @value.setter
    def value (self, v) :
        fv = float(v)
        self._value = fv % 360.0 if fv > 360.0 else fv % -360 if fv < -360.0 else fv

    @property
    def v (self) :
        return self._value  # a brief alias for value, readonly

    @property
    def deg (self) :
        return "{:12.7f}".format(self.value)

    @property
    def dms (self) :
        return self.dec2dms(self.value)

    @property
    def hms (self) :
        return self.dec2hms(self.value)

    @property
    def hour (self) :
        return self.hour2str(self.value / 15.0)

    @property
    def dtype (self) :
        return self._dtype

    def __repr__ (self) :
        if self._dtype == "deg" :
            return self.deg
        elif self._dtype == "hour" :
            return self.hour
        elif self._dtype == "ra" :
            return self.hms
        else :
            return self.dms

    def __float__ (self) :
        return self.value

    def __add__ (self, other) :
        return xangle(self.value + float(other), dtype=self._dtype)
    def __radd__ (self, other) :
        return self + other

    def __sub__ (self, other) :
        return xangle(self.value - float(other), dtype=self._dtype)
    def __rsub__ (self, other) :
        return self - other

    def __iadd__ (self, other) :
        self.value += float(other)
        return self
    def __isub__ (self, other) :
        self._value -= float(other)
        return self

    def __anglecmp (self, other) :
        d = (self.value - float(other)) % 360.0
        return 0 if d == 0.0 else 1 if d <= 180.0 else -1
    def __lt__ (self, other) :
        return self.__anglecmp(other) < 0
    def __le__ (self, other) :
        return self.__anglecmp(other) <= 0
    def __gt__ (self, other) :
        return self.__anglecmp(other) > 0
    def __ge__ (self, other) :
        return self.__anglecmp(other) >= 0
    def __eq__ (self, other) :
        return self.__anglecmp(other) == 0
    def __ne__ (self, other) :
        return self.__anglecmp(other) != 0

    @staticmethod
    def dms2dec ( dms, delimiter=":" ) :
        """ Transform deg:min:sec format angle to decimal format
        args:
            dms: sexagesimal angle string, format +/-dd:mm:ss.xxx
            delimiter: char seperate deg, min and sec, default is ":"
        returns:
            decimal angle in degree
        """
        pp = dms.split(delimiter)
        if len(pp) >= 3 :
            ss = float(pp[2])
        else :
            ss = 0.0
        if len(pp) >= 2 :
            mm = float(pp[1])
        else :
            mm = 0.0
        hh = abs(float(pp[0]))
        pm = -1.0 if dms[0] == "-" else 1.0

        dec = pm * (hh + mm / 60.0 + ss / 3600.0)
        return dec

    @staticmethod
    def hms2dec ( hms, delimiter=":" ) :
        """ Transform hour:min:sec format angle to decimal format
        args:
            hms: sexagesimal angle string, format hh:mm:ss.xxx
            delimiter: char seperate deg, min and sec, default is ":"
        returns:
            decimal angle in degree
        """
        dec = xangle.dms2dec(hms, delimiter) * 15.0
        return dec

    @staticmethod
    def dec2dms ( dec, len=11, delimiter=":" ) :
        """ Transform decimal format angle to deg:min:sec format
        args:
            dec: decimal angle in degree
            len: output length of string
            delimiter: char seperate deg, min and sec, default is ":"
        returns:
            sexagesimal angle string, format +/-dd:mm:ss.xxx
        """
        dec0 = dec % 360.0 if dec >= 0.0 else dec % -360.0
        pm = "-" if dec0 < 0.0 else "+"
        adec = abs(dec0)
        dd = int(adec)
        mm = int((adec - dd) * 60.0)
        ss = (adec - dd) * 3600 - mm * 60.0
        dms = "{n:1s}{d:02d}{l}{m:02d}{l}{s:08.5f}".format(n=pm, d=dd, m=mm, s=ss, l=delimiter)
        return dms[0:len]

    @staticmethod
    def dec2hms ( dec, len=11, delimiter=":" ) :
        """ Transform decimal format angle to deg:min:sec format
        args:
            dec: decimal angle in degree
            len: output length of string
            delimiter: char seperate deg, min and sec, default is ":"
        returns:
            sexagesimal angle string, format hh:mm:ss.xxx
        """
        hh = (dec % 360.0) / 15.0
        hms = xangle.dec2dms(hh, len+1, delimiter)
        return hms[1:]

    @staticmethod
    def hour2str ( hr, delimiter=":" ) :
        """ Transfer hours to hh:mm format string
        args:
            hr: hours, 0.0 to 36.0, will error for negative
            delimiter: char seperate deg, min and sec, default is ":"
        returns:
            string hours and minutes, in hh:mm format
        """
        mi = int(round(hr * 60))
        hh = int(mi / 60)
        mm = int(mi % 60)
        s = "{h:02d}{l}{m:02d}".format(h=hh, m=mm, l=delimiter)
        return s


class xra (xangle) :
    def __init__ (self, value, format="deg", delimiter=":", dtype="ra") :
        xangle.__init__(self, value, format=format, delimiter=delimiter, dtype=dtype)
        if self._value < 0 : self._value += 360.0


class xdec (xangle) :
    def __init__ (self, value, format="deg", delimiter=":", dtype="dec") :
        xangle.__init__(self, value, format=format, delimiter=delimiter, dtype=dtype)
        if self._value >  90.0 : self._value =  90.0
        if self._value < -90.0 : self._value = -90.0


class xlon (xangle) :
    def __init__ (self, value, format="deg", delimiter=":", dtype="lon") :
        xangle.__init__(self, value, format=format, delimiter=delimiter, dtype=dtype)


class xlat (xangle) :
    def __init__ (self, value, format="deg", delimiter=":", dtype="lat") :
        xangle.__init__(self, value, format=format, delimiter=delimiter, dtype=dtype)
        if self._value >  90.0 : self._value =  90.0
        if self._value < -90.0 : self._value = -90.0


class xgl (xangle) :
    def __init__ (self, value, format="deg", delimiter=":", dtype="gl") :
        xangle.__init__(self, value, format=format, delimiter=delimiter, dtype=dtype)


class xgb (xangle) :
    def __init__ (self, value, format="deg", delimiter=":", dtype="gb") :
        xangle.__init__(self, value, format=format, delimiter=delimiter, dtype=dtype)
        if self._value >  90.0 : self._value =  90.0
        if self._value < -90.0 : self._value = -90.0


class xhour (xangle) :
    def __init__ (self, value, format="hour", delimiter=":", dtype="hour") :
        xangle.__init__(self, value, format=format, delimiter=delimiter, dtype=dtype)

