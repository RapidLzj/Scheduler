"""
    Cut SDSS covered area from nowt plan
"""

import numpy as np


if __name__ == "__main__" :
    fldxao = np.loadtxt("field.xao.new.txt", usecols=(0,1,2,3,4))

    fmt = " %5d  %9.5f  %9.5f  %9.5f  %9.5f \n"
    f = open("field.xao.sdss.txt", "w")
    for fld in fldxao :
        fid, fra, fdec, fgl, fgb = int(fld[0]), fld[1], fld[2], fld[3], fld[4]

        if (fgb > 0 and (fra < 135 or fdec > 65)) or \
           (fgb < 0 and (fdec > 30 or (30 < fra and fra < 330))) :
           f.write(fmt % (fid, fra, fdec, fgl, fgb))
    f.close()
