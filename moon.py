# -*- coding: utf-8 -*-
"""
    Module Moon
    Function about moon, position, and phase
    v1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    Providing:
        moon_pos
        sun_pos
        moon_phase
"""


import astropy.coordinates
import astropy.time
import numpy as np


class position :
    """ A simple class holding the ra, dec, and distance
    """

    def __init__ ( self, ra, dec, dis ) :
        self.ra  = ra
        self.dec = dec
        self.dis = dis

    def __repr__ ( self ) :
        return "{r:>10.6f} {d:>+10.6f} {s}".format(r=self.ra, d=self.dec, s=self.dis)


def moon_pos ( mjd ) :
    p = astropy.coordinates.get_moon(astropy.time.Time(mjd, format="mjd"))
    pd = position(p.ra.deg, p.dec.deg, p.distance.km)
    return pd


def sun_pos ( mjd ) :
    p = astropy.coordinates.get_sun(astropy.time.Time(mjd, format="mjd"))
    pd = position(p.ra.deg, p.dec.deg, p.distance.km)
    return pd


def moon_phase ( mjd ) :
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
    phi = np.arccos( np.sin(decs) * np.sin(decm) + np.cos(decs) * np.cos(decm) * np.cos(ras - ram) )
    inc = np.arctan2( diss * np.sin(phi), dism - diss * np.cos(phi) )
    p = (1 + np.cos(inc)) / 2.0
    return p


def moon_phase2 ( yr, mn, dy, hr=0, mi=0, se=0, tz=0 ) :
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
    lunar_day = ( year_corr[(yr + 1) % 19] + month_corr[mn-1] + dy + hh ) % 30.0
    phase = 2.0 * lunar_day / 29.0
    if phase > 1.0:
        phase = abs(phase - 2.0)
    return phase


def distance ( ra1, de1, ra2, de2 ) :
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
        np.sin(dde / 2.0) ** 2.0 + np.cos(de1) * np.cos(de2) * np.sin(dra / 2.0) ** 2 ))
    return np.rad2deg(delta)
