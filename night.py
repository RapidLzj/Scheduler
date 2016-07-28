import math


def d2r(d) :
    return d / 180.0 * math.pi


def r2d(r) :
    return r / math.pi * 180.0


def d2s(d) :
    mi = round(d * 60)
    h = int(mi / 60)
    m = int(mi % 60)
    return "{:02d}:{:02d}".format(h, m)


def night() :
    dm = [31, 29, 31,  30, 31, 30,  31, 31, 30,  31, 30, 31]
    lat = d2r(31.963)
    d0 = 10 # day no to Winter Solstice
    mjd16=7388
    for m in range(0, 12) :
        for d in range(0, dm[m]) :
            d0 += 1
            mjd16 += 1
            mjd17 = mjd16 + (366 if m < 2 else 366)
            dpos = (d0 / 365.24) * 2 * math.pi
            spos = d2r(-23.5) * math.cos(dpos)
            sunris = math.acos(math.tan(lat) * math.tan(spos)) / math.pi * 12
            sunset = 24 - sunris
            daylen = sunset - sunris
            #print ("J{:04d} {:02d}-{:02d}  {}==>{}, <=> {}  D/Y{:5.3f} S_Dec{:5.1f}  OBS: {:02d}-{:02d}".
            #       format(mjd, m+1,d+1, d2s(sunris), d2s(sunset),
            #       d2s(daylen), dpos/2/math.pi, r2d(spos),
            #       d2s(sunris-1), d2s(sunset+1)))
            print ("2016, {:02}, {:02}, {}, {}, {:04}, {:04}".format(
                   m+1, d+1, d2s(sunset+1.25), d2s(sunris-1.25), mjd16, mjd17))



if __name__ == "__main__" :
    night()