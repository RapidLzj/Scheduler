

if __name__ == "__main__" :
    f = open("field.bok.txt", "r")
    lines = f.readlines()
    f.close()

    fmt = " %5d  %9.5f  %9.5f  %9.5f  %9.5f \n"
    f = open("field.bok.new.txt", "w")
    for line in lines :
        part = line.split()
        fid =int(part[2])
        fra, fdec = float(part[0]), float(part[1])
        fgl, fgb = float(part[4]), float(part[5])

        if fgb < 0 or (fgl > 0 and fra < 181) :
            f.write(fmt % (fid, fra, fdec, fgl, fgb))

    f.close()
