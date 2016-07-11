function zj_dec2hmsd, d
    n = d ge 0.0
    dd = long(abs(d) * 360000.0)
    h = dd / 360000
    m = dd / 6000 mod 60
    s = dd / 100 mod 60
    k = dd mod 100
    ;h = fix(abs(d))
    ;m = fix((abs(d) - h) * 60.0)
    ;s = fix((abs(d) - h - m / 60.0) * 3600.0)
    ;k = fix((abs(d) - h - m / 60.0 - s * 3600.0) * 360000.0)
    return, [n, h, m, s, k]
end

function zj_radec2str, ra, dec
    ; convert ra&dec to string format, format related different telescope control system
    ; bok: hhmmss.dd +ddmmss.d
    ; xao: hh:mm:ss.dd  +dd:mm:ss.d
    rax  = zj_dec2hmsd(ra / 15.0)
    decx = zj_dec2hmsd(dec)
    ras  = string(rax[1:3], rax[4], format='(3I2.2,".",I2.2)')
    decs = string((decx[0]?'+':'-'), decx[1:3], decx[4]/10, format='(A1,3I2.2,".",I1.1)')
    ;ras  = string(rax[1:3], rax[4], format='(I2.2,":",I2.2,":",I2.2,".",I2.2)')
    ;decs = string((decx[0]?'+':'-'), decx[1:3], decx[4]/10, format='(A1,I2.2,":",I2.2,":",I2.2,".",I1.1)')
    return, [ras, decs]
end