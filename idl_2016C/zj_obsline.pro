function zj_obsline, fid, filter, expt, fra, fdec
    return, string(expt, fid, filter, zj_radec2str(fra, fdec), $
        format='("obs  ",F5.1,"  object  ",A8,"  1  ",A,"  ",A,"  ",A,"  2000.0")')
end