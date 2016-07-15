"""
    Remove spring and summer part from original plan
"""

if __name__ == "__main__" :
    f = open("field.xao.txt", "r")
    lines = f.readlines()
    f.close()

    fmt = " %5d  %9.5f  %9.5f  %9.5f  %9.5f  %s  %s \n"
    f = open("field.xao.new.txt", "w")
    for line in lines :
        part = line.split()
        fid =int(part[0])
        fra, fdec = float(part[1]), float(part[2])
        fgl, fgb = float(part[3]), float(part[4])
        fras, fdecs = part[5], part[6]

        if fdec > -2 and (fgb < 0 or (fgl > 0 and fra < 181)) :
            f.write(fmt % (fid, fra, fdec, fgl, fgb, fras, fdecs))

    f.close()
