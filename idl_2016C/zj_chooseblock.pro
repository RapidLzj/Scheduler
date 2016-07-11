function zj_chooseblock, ra, dec, alt
    ix1 = where(alt lt 80.0 and alt gt 60.0, nix)
    if nix eq 0 then return, -1

    ix2 = where(dec[ix1] eq min(dec[ix1]))
    ix3 = ix1[ix2]

    ix4 = where(alt[ix3] eq max(alt[ix3]))
    ix5 = ix3[ix4]

    return, ix5[0]
end