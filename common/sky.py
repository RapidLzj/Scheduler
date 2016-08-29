# -*- coding: utf-8 -*-
"""
    2016-06-17, 2016M-1.0 lzj
    Utilities for pipeline, general operations
    This part including sky coordination operations, but no angle transform
"""


import astropy.coordinates
from astropy.time import Time
import numpy as np
from .info import info


class position (info) :
    """ A simple class holding the ra, dec, and distance
    """

    def __init__ (self, ra, dec, dis) :
        info.__init__(self, "Position", ra=ra, dec=dec, dis=dis)

    def __repr__ (self) :
        return "{r:>10.6f} {d:>+10.6f} {s}".format(r=self.ra, d=self.dec, s=self.dis)


def moon_pos (mjd) :
    """ Moon position, call astropy
    args:
        mjd: mjd
    returns:
        position instance, with ra, dec, distance
    """
    p = astropy.coordinates.get_moon(Time(mjd, format="mjd"))
    pd = position(p.ra.deg, p.dec.deg, p.distance.km)
    return pd


def sun_pos (mjd) :
    """ Sun position, call astropy
    args:
        mjd: mjd
    returns:
        position instance, with ra, dec, distance
    """
    p = astropy.coordinates.get_sun(Time(mjd, format="mjd"))
    pd = position(p.ra.deg, p.dec.deg, p.distance.km)
    return pd


def moon_phase (mjd) :
    """ get moon phase at given time
        method from MPHASE.pro in astron lib for IDL
    """
    #diss = 1.49598e8         #Earth-Sun distance (1 AU)

    mp = moon_pos (mjd)
    sp = sun_pos(mjd)
    ram  = np.deg2rad(mp.ra)
    decm = np.deg2rad(mp.ra)
    dism = mp.dis
    ras  = np.deg2rad(sp.ra)
    decs = np.deg2rad(sp.ra)
    diss = sp.dis

    # phi - geocentric elongation of the Moon from the Sun
    # inc - selenocentric (Moon centered) elongation of the Earth from the Sun
    phi = np.arccos(np.sin(decs) * np.sin(decm) + np.cos(decs) * np.cos(decm) * np.cos(ras - ram))
    inc = np.arctan2(diss * np.sin(phi), dism - diss * np.cos(phi))
    p = (1 + np.cos(inc)) / 2.0
    return p


def moon_phase2 (yr, mn, dy, hr=0, mi=0, se=0, tz=0) :
    """ get moon phase at given time
    https://www.daniweb.com/programming/software-development/code/453788/moon-phase-at-a-given-date-python
    args:
        yr: year
        mn: month
        dy: day
        hr: hour
        mi: minute
        se: second
        tz: timezone
    returns:
        moonphase, 0.0 to 1.0
    """
    hh = hr + mi / 60.0 + se / 3600.0 - tz
    year_corr = [18, 0, 11, 22, 3, 14, 25, 6, 17, 28, 9, 20, 1, 12, 23, 4, 15, 26, 7]
    month_corr = [-1, 1, 0, 1, 2, 3, 4, 5, 7, 7, 9, 9]
    lunar_day = (year_corr[(yr + 1) % 19] + month_corr[mn-1] + dy + hh) % 30.0
    phase = 2.0 * lunar_day / 29.0
    if phase > 1.0:
        phase = abs(phase - 2.0)
    return phase


def distance (ra1, de1, ra2, de2) :
    """ Fast distance between point1 (ra1,de1) and point2 (ra2,de2)
        Rewrite this because seperation in astropy is too slow for many objects
        Use haversine formula from wikipedia
    args:
        ra1: ra of point 1, in degrees
        de1: dec of point 1
        ra2: ra of point 2, in degrees
        de2: dec of point 2
    returns:
        distance betewwn points, in degrees
    note: 1 and 2 can be scalar or ndarray, but if both are array, they must have same shape
    """
    ra1, de1 = np.deg2rad(ra1), np.deg2rad(de1)
    ra2, de2 = np.deg2rad(ra2), np.deg2rad(de2)
    dra = np.abs(ra1 - ra2) # lambda
    dde = np.abs(de1 - de2) # phi
    delta = 2.0 * np.arcsin(np.sqrt(
        np.sin(dde / 2.0) ** 2.0 + np.cos(de1) * np.cos(de2) * np.sin(dra / 2.0) ** 2))
    return np.rad2deg(delta)


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
    dofy = sum(md[0:mn]) + dy  # day of year
    if yr % 4 == 0 and mn > 2 : dofy += 1 # leap year
    return dofy


def lst (mjd, lon) :
    """ get local sidereal time for longitude at specidied mjd
    args:
        mjd: mjd
        lon: longitude, in degrees
    returns:
        lst: in hours
    """
    return Time(mjd, format="mjd").sidereal_time("mean", lon).hour


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


def hourangle (lst, ra) :
    """ Calculate hourangle of specified ra, -12 to +12
    args:
        lst: local sidereal time, in hours
        ra: ra of object, in degrees
    returns:
        hourangle, in hours, -12 to +12
    """
    return (lst - ra / 15.0 + 12.0) % 24.0 - 12.0


def airmass (lat, lst, ra, dec) :
    """ Calculate airmass
        Use simplified formula from old obs4, unknown source
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
    if type(x) == np.ndarray :
        x[np.where((x < 0.0) | (x > 9.99))] = 9.99
    else :
        if (x < 0.0) or (x > 9.99) :
            x = 9.99

    return x


def azalt (lat, lst, ra, dec) :
    """ Convert RA/Dec of object to Az&Alt
        Use formular from hadec2altaz of astron of IDL
    args:
        lat: latitude of site, in degrees
        lst: local sidereal time, in hours
        ra: ra of target, in degrees, scrlar or ndarray
        dec: dec of target, same shape as ra
    returns:
        az, alt
    """
    lat = np.deg2rad(lat)
    lst = np.deg2rad(lst * 15.0)
    ra  = np.deg2rad(ra)
    dec = np.deg2rad(dec)
    ha = lst - ra

    sh = np.sin(ha)
    ch = np.cos(ha)
    sd = np.sin(dec)
    cd = np.cos(dec)
    sl = np.sin(lat)
    cl = np.cos(lat)

    x = - ch * cd * sl + sd * cl
    y = - sh * cd
    z = ch * cd * cl + sd * sl
    r = np.sqrt(x * x + y * y)

    az  = np.rad2deg(np.arctan2(y, x)) % 360.0
    alt = np.rad2deg(np.arctan2(z, r))

    return az, alt


def mjd_of_night (yr, mn, dy, site) :
    """ get 4-digit mjd code for the site, using local 18:00
    args:
        yr: year
        mn: month
        dy: day
        site: site object
    returns:
        jjjj, 4 digit of mjd at local 18:00
    """
    j = int(mjd(yr, mn, dy, 18, 0, 0, site.tz)) % 10000
    return j


def mjd2hour(mjd, tz=0) :
    """ Extract hour part from mjd"""
    h = (mjd * 24.0 + tz) % 24.0
    return h


def sun_action (mjd24, lst24, lat, palt=0.0) :
    """ Get time of sun pass specified altitude, in this night
        Use grid to estimate, precise to 0.001, about 1.44 min (86.4sec)
        Assume midnight sun is lower than palt, no polor night or polar day
    args:
        mjd24: mjd of midnight
        lst24: local sidereal time of midnight. (in takeoff, this is already calculated)
        lat: latitude of site
        palt: altitude of sun passing, default 0, means sunset and sunrise
    returns:
        sunset, sunrise: tuple of mjd of sun set and rise time
    """
    sp = sun_pos(mjd24)
    # backward to get sunset time
    mjdse = mjd24
    lstse = lst24
    for step in (0.1, 0.01, 0.001) :
        while True :
            az, alt = azalt(lat, lstse - step * 24.0, sp.ra, sp.dec)
            # when sun first time higher than palt, break, mjdse and lstse are last value under
            if alt > palt: break
            #print lstse, alt
            mjdse -= step
            lstse -= step * 24.0
    # forward to get sunrise time
    mjdsr = mjd24
    lstsr = lst24
    for step in (0.1, 0.01, 0.001) :
        while True :
            az, alt = azalt(lat, lstsr + step * 24.0, sp.ra, sp.dec)
            # when sun first time higher than palt, break, mjdse and lstse are last value under
            if alt > palt: break
            #print lstsr, alt
            mjdsr += step
            lstsr += step * 24.0
    return mjdse, mjdsr
